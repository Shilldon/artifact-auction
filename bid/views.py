import json, datetime
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from decimal import Decimal
from .forms import BiddingForm
from .models import Bids
from artifacts.models import Artifact
from auctions.models import Auction

""" Take a bid from the user and check if higher than current bid """
def check_bid(request, bid_form, artifact):
    auction = get_object_or_404(Auction, artifact=artifact)
    
    if bid_form.is_valid():
        new_bid = Decimal(request.POST['amount_bid'])
        current_bid = Decimal(auction.current_bid)
        if new_bid > current_bid:
            
            """send email to  previous bidder regarding bid status"""
            bid_email(request, artifact, new_bid)
            
            """check if there are any existing bids in the auction by artifact look up"""
            """auction and bid have the artifact model in common"""
            queryset = Bids.objects.filter(auction=auction)
            bid = Bids(bid_amount=new_bid, bidder=request.user, auction=auction)
            bid.time = datetime.datetime.now()
            bid.save()
            
            auction.current_bid = new_bid    
            auction.current_bidder = request.user

            if new_bid > auction.reserve_price:
                auction.reserve_price = Decimal(new_bid) * Decimal(1.2)
                artifact.buy_now_price = auction.reserve_price
                artifact.save()
                
            auction.save()


            messages.success(request, 
                             "You have successfully placed your bid on %s" %artifact.name)
            return True
            
        else:
            messages.error(request,
                           "Your offer needs to be higher than the current bid")
            return False

def bid_email(request, artifact, new_bid):
    auction = get_object_or_404(Auction, artifact=artifact)
    email_title = 'Artifact Auctions - '+artifact.name
    email_message = 'You have been outbid on '+artifact.name+'. The current bid is now £'+str(new_bid)+'.'
    if auction.current_bidder:
        send_mail(
        email_title,
        email_message,
        'admin@artifact-auction.com',
        [auction.current_bidder.email],
        fail_silently=False,)      
        
"""return current bid value on artifact"""
def get_bid(request):
    if request.method == "GET":
        id = request.GET["artifact_id"]
        artifact = get_object_or_404(Artifact, pk=id)
        try:
            auction = get_object_or_404(Auction, artifact=artifact)
            response_data = {}
            """no need to pass reserve price - if bid is higher then page will reload which will update the reserve price"""
            response_data['current_bid'] = float(auction.current_bid)
            response_data['start_time'] = str(auction.start_date)
            response_data['end_time'] = str(auction.end_date)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            return HttpResponse("unsucessful")