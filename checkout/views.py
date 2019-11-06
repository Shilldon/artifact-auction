from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from artifacts.models import Artifact
from auctions.models import Auction
from bid.models import Bids
from .forms import MakePaymentForm, OrderForm
from .models import PurchasedArtifact
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def checkout(request):

    if request.method=="POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            collection = request.session.get('collection', {})
            #a check list to add artifacts to which might have been purchased
            #by another user before the current user got to the checkout.
            artifacts_already_sold = []
            #a list of artifacts the current user has successfully purchased
            #to iterate in order to update the artifacts status.
            artifacts_purchased = []
            
            total = 0
            an_artifact_was_sold = False
            
            for id, price in collection.items():
                artifact = get_object_or_404(Artifact, pk=id)
                if artifact.sold is not True:
                    total += price
                    artifacts_purchased.append(artifact)
                    order_line_item = PurchasedArtifact(
                        order = order,
                        artifact = artifact,
                        )
                    order_line_item.save()
                else:
                    #if the artifact has sold add it to the list of sold
                    #artifacts
                    an_artifact_was_sold = True
                    messages.error(request, "Sorry "+artifact.name+" has been already been purchased by another user.")    
                    artifacts_already_sold.append(id)
            
            #iterate through the artifacts already sold to another user and
            #remove them from this user's collection.
            if len(artifacts_already_sold) > 0:
                for id in artifacts_already_sold:
                    collection.pop(id, None)
                request.collection = collection
            
            #after removing sold artifacts check if there are any remaining and,
            #if so, let the user know the purchase order has been updated
            #else proceed with purchase
            if bool(collection) is False:
                messages.error(request, "You have no artifacts in your collection to purchase")    
            elif an_artifact_was_sold:
                messages.error(request, "Your purchase order has been updated.")
            else:
                try:
                    customer = stripe.Charge.create(
                        amount= int(total * 100), 
                        currency = "GBP",
                        description = request.user.email,
                        card = payment_form.cleaned_data['stripe_id'],
                    )
                except stripe.error.CardError:
                    customer = None
                    messages.error(request, "Your card was declined")
                
                if customer.paid:
                    for artifact in artifacts_purchased:
                        artifact.sold = True
                        artifact.owner = request.user
                        artifact.save()                    
                        auction = get_object_or_404(Auction, artifact=artifact)
                        auction.delete()
                    request.session['collection'] = {}
                        
                    #create a string of the artifacts purchased to email to
                    #purchaser
                    list_of_artifacts = []
                    for artifact in artifacts_purchased[:-1]:
                        list_of_artifacts.append(artifact.name+",")
                    last_artifact = artifacts_purchased[-1]
                    list_of_artifacts.append("and "+last_artifact.name)
                        
                    email_artifacts_purchased = ' '.join(list_of_artifacts).lstrip()
                    email_title = 'Artifact Auctions - Your purchase'
                    email_message_purchase = 'Thank you for purchasing '+email_artifacts_purchased+'. Your purchase will be delivered to you in 3-4 working days.'
                    send_mail(
                        email_title,
                        email_message_purchase,
                        'admin@artifact-auction.com',
                        [artifact.owner.email],
                        fail_silently=False,)  
                    messages.error(request, "You have successfully paid")
                    return redirect(reverse('artifacts_list'))
                else:
                    messages.error(request, "We were unable to take payment with that card.")
        else:
            messages.error(request, "Unable to take payment. Please try again.")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()

    return render(request, "checkout.html", {'order_form' : order_form, 'payment_form' : payment_form, 'publishable': settings.STRIPE_PUBLISHABLE })
    

def buy_all(request):
    """
    On selecting pay for all won artifacts. Cycle through artifacts won
    and add to collection then proceed to checkout
    """
    collection = {}
    finished_auctions = Auction.objects.filter(end_date__lte=timezone.now())
    highest_bids = []
    
    for auction in finished_auctions:
        try:
            bids = Bids.objects.filter(auction=auction)
            highest_bid = bids.order_by('-bid_amount')[0]
            highest_bids.append(highest_bid)
        except:
            None
    
    for bid in highest_bids:
        if bid.bidder == request.user:
            artifact = bid.auction.artifact
            id = artifact.id
            price = float(bid.bid_amount)
            collection[id] = collection.get(id, price)
            request.session['collection'] = collection        

    return redirect(reverse('checkout'))    
    
def buy_one(request, id, buy_now):
    """
    Get the user's collection of artifacts and, if not already in the collection 
    add the selected artifact to the collection
    """
    print("HERE")
    artifact = get_object_or_404(Artifact, pk=id)
    auction = get_object_or_404(Auction, artifact=artifact)
    price = 0
    collection = {}
    """
    On selecting pay now or buy now for a single artifact determine the
    price and proceed to checkout just for that artifact
    """
    if int(buy_now)==1:
        price = float(artifact.buy_now_price)
    else:
        last_bid = Bids.objects.filter(auction=auction).order_by('-bid_amount')[0].bid_amount
        price = float(last_bid)

    collection[id] = collection.get(id, price)
    request.session['collection']=collection


    return redirect(reverse('checkout'))    