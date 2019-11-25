import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils import timezone
from .forms import MakePaymentForm, OrderForm
from .models import PurchasedArtifact
from artifacts.models import Artifact
from auctions.models import Auction, Bid

stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    """
    A view to process payment for artifacts selected

    Only render checkout if the user is logged in
    """
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            basket = request.session.get('collection', {})
            """
            Create a list to add artifacts to which might have been
            purchased by another user before the current user got to the
            checkout (through buy now option).
            """
            artifacts_already_sold = []
            """
            Create a blank list of artifacts that the current user has
            successfully purchased to iterate through in order to update the
            artifacts sold status after clearing payment.
            """
            artifacts_purchased = []

            total = 0
            an_artifact_was_sold = False
            for id, value in basket.items():
                """
                iterate through basket and check whether artifacts have been
                sold. If not total up the price and set the sale price
                on the artifact model.
                """
                artifact = get_object_or_404(Artifact, pk=id)
                if artifact.sold is not True:
                    total += value['price']
                    artifacts_purchased.append(
                                               {
                                                'artifact': artifact,
                                                'buy_now': value['buy_now']
                                                }
                                               )
                    artifact.purchase_price = value['price']
                    order_line_item = PurchasedArtifact(
                        order=order,
                        artifact=artifact,
                        )
                    order_line_item.save()
                else:
                    """
                    if an artifact has been sold already add it to the list of
                    sold artifacts
                    """
                    an_artifact_was_sold = True
                    messages.error(request,
                                   "Sorry " + artifact.name +
                                   " has been already been purchased by "
                                   "another user.")
                    artifacts_already_sold.append(id)

            """
            Iterate through the artifacts already sold to another user and
            remove them from this user's basket.
            """
            if len(artifacts_already_sold) > 0:
                for id in artifacts_already_sold:
                    basket.pop(id, None)
                request.session['collection'] = basket

            """
            After removing sold artifacts check if there are any remaining and,
            if so, let the user know the purchase order has been updated
            else proceed with purchase
            """
            if bool(basket) is False:
                messages.error(request,
                               "You have no artifacts in your collection"
                               "to purchase")
            elif an_artifact_was_sold:
                messages.error(request, "Your purchase order has been "
                                        "updated.")
            else:
                try:
                    customer = stripe.Charge.create(
                        amount=int(total * 100),
                        currency="GBP",
                        description=request.user.email,
                        card=payment_form.cleaned_data['stripe_id'],
                    )
                except stripe.error.CardError:
                    customer = None
                    messages.error(request, "Your card was declined")
                if customer.paid:
                    for item in artifacts_purchased:
                        artifact = item['artifact']
                        artifact.sold = True
                        artifact.owner = request.user
                        artifact.buy_now_price = 0
                        artifact.save()
                        auction = get_object_or_404(Auction, artifact=artifact)
                        if int(item['buy_now']) == 1:
                            """
                            Send email to the highest bidder to inform them
                            that the artifact has been purchased
                            """
                            bids = Bid.objects.filter(auction=auction)
                            try:
                                bids = Bid.objects\
                                          .filter(auction=auction)\
                                          .exclude(bidder=request.user)
                                highest_bid = bids.order_by('-bid_amount')[0]
                                bidder = highest_bid.bidder
                                email_title = 'Artifact Auctions - Your Bid'
                                email_message_sold = 'Thank you for your '\
                                                     'interest in ' + \
                                                     artifact.name + \
                                                     '. Unfortunately another'\
                                                     ' user has directly '\
                                                     'purchased this artifact.'
                                send_mail(
                                    email_title,
                                    email_message_sold,
                                    'admin@artifact-auction.com',
                                    [bidder.email],
                                    fail_silently=False,)
                            except:
                                None
                        """
                        Now the artifact has been purchased delete the auction
                        instance
                        """
                        auction.delete()

                    """
                    Clear the user's basket
                    """
                    request.session['collection'] = {}
                    """
                    create a string of the artifacts purchased to email to
                    purchaser
                    """
                    list_of_artifacts = []
                    if len(artifacts_purchased) > 1:
                        for item in artifacts_purchased[:-1]:
                            list_of_artifacts.append(item['artifact'].name+",")
                        last_artifact = artifacts_purchased[-1]['artifact']
                        list_of_artifacts.append("and "+last_artifact.name)
                    else:
                        list_of_artifacts.append(artifacts_purchased[0]
                                                 ['artifact'].name)

                    email_artifacts_purchased = ' '.join(list_of_artifacts)\
                                                   .lstrip()
                    email_title = 'Artifact Auctions - Your purchase'
                    email_message_purchase = ('Thank you for purchasing ' +
                                              email_artifacts_purchased +
                                              '. Your purchase will be '
                                              'delivered to you in 3-4 working'
                                              ' days.')
                    send_mail(
                        email_title,
                        email_message_purchase,
                        'admin@artifact-auction.com',
                        [artifact.owner.email],
                        fail_silently=False,)
                    messages.success(request,
                                     'Thank you for purchasing ' +
                                     email_artifacts_purchased + '.')
                    return redirect(reverse('artifacts_list'))
                else:
                    messages.error(request,
                                   "We were unable to take payment with that"
                                   " card.")
        else:
            messages.error(request, "Unable to take payment. Please try "
                                    "again.")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()

    return render(request,
                  "checkout.html",
                  {'order_form': order_form,
                   'payment_form': payment_form,
                   'publishable': settings.STRIPE_PUBLISHABLE}
                  )


def buy_all(request):
    """
    A view to add all artifacts the user has won but not paid for to their
    basket and then proceed to payment
    Check the auctions that the user has won and add those artifacts to the
    basket
    """

    basket = {}
    finished_auctions = Auction.objects.filter(end_date__lte=timezone.now())
    highest_bids = []
    for auction in finished_auctions:
        try:
            bids = Bid.objects.filter(auction=auction)
            highest_bid = bids.order_by('-bid_amount')[0]
            highest_bids.append(highest_bid)
        except:
            None

    """
    Get the highest bid value and set that as the price for each artifact
    """

    for bid in highest_bids:
        if bid.bidder == request.user:
            artifact = bid.auction.artifact
            id = artifact.id
            price = float(bid.bid_amount)
            basket[id] = basket.get(id, {'price': price, 'buy_now': 0})
            request.session['collection'] = basket

    return redirect(reverse('checkout'))


def buy_one(request, id, buy_now):
    """
    A view to add a single artifact the user won or selected to buy now to
    their basket and then proceed to payment.

    Clear the user's basket add the one artifact selected to buy now to the
    basket then proceed to the checkout.
    """
    artifact = get_object_or_404(Artifact, pk=id)
    auction = get_object_or_404(Auction, artifact=artifact)
    price = 0
    basket = {}
    """
    On selecting pay now or buy now for a single artifact determine the
    price and proceed to checkout just for that artifact.
    The price will either be the buy now value or highest bid depending on
    whether the user selected buy now or won the artifact.
    """
    if int(buy_now) == 1:
        price = float(artifact.buy_now_price)
    else:
        last_bid = Bid.objects.filter(auction=auction)\
                      .order_by('-bid_amount')[0].bid_amount
        price = float(last_bid)

    basket[id] = basket.get(id, {'price': price, 'buy_now': buy_now})
    request.session['collection'] = basket

    return redirect(reverse('checkout'))
