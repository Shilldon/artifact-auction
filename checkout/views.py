from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from artifacts.models import Artifact
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
            total = 0
            id = collection['purchase']
            artifact = get_object_or_404(Artifact, pk=id)
            total = artifact.price

            if artifact.sold is False:            
                order_line_item = PurchasedArtifact(
                    order = order,
                    artifact = artifact,
                    )
                order_line_item.save()
    
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
                    artifact.sold = True
                    artifact.owner = request.user
                    artifact.listed_date = None
                    artifact.auction_end_date = None
                    artifact.bid = 0
                    artifact.current_bidder = None
                    artifact.reserved = False
                    artifact.save()
                    request.session['collection'] = {}
                    
                    email_title = 'Artifact Auctions - '+artifact.name
                    email_message_purchase = 'Thank you for purchasing '+artifact.name+'. The artifact will be delievered to you in 3-4 working days.'
                    send_mail(
                        email_title,
                        email_message_purchase,
                        'admin@artifact-auction.com',
                        [artifact.owner],
                        fail_silently=False,)  
                    
                    messages.success(request, "You have successfully paid")
                    return redirect(reverse('artifacts_list'))
                else:
                    messages.error(request, "Unable to take payment")
                
            else:
                print(payment_form.errors)
                messages.error(request, "We were unable to take payment with that card.")
        else:
            messages.error(request, "Sorry, that artifact has been sold")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        
    return render(request, "checkout.html", {'order_form' : order_form, 'payment_form' : payment_form, 'publishable': settings.STRIPE_PUBLISHABLE })