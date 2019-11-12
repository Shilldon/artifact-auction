# -*- coding: utf-8 -*-
import json, datetime
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from decimal import Decimal
from .forms import BiddingForm
from .models import Bid
from artifacts.models import Artifact
from auctions.models import Auction

""" Take a bid from the user and check if higher than current bid """
def check_bid(request, bid_form, artifact):
    auction = get_object_or_404(Auction, artifact=artifact)
    
    if bid_form.is_valid():
        new_bid = Decimal(request.POST['amount_bid'])
        bids = Bid.objects.filter(auction=auction)
        try:
            current_bid = bids.order_by('-bid_amount')[0].bid_amount
        except:
            current_bid = 0
        if new_bid > current_bid:
            """send email to  previous bidder regarding bid status"""
            bid_email(request, artifact, new_bid)
            
            """check if there are any existing bids in the auction by artifact look up"""
            """auction and bid have the artifact model in common"""
            bid = Bid(bid_amount=new_bid, bidder=request.user, auction=auction)
            bid.time = datetime.datetime.now()
            bid.save()
            
            if new_bid > artifact.buy_now_price:
                artifact.buy_now_price = Decimal(new_bid) * Decimal(1.2)
                artifact.save()

            messages.success(request, 
                             "Thank you for your bid on %s. You will be notified by email if you are outbid." % (artifact.name))
            return True
            
        else:
            messages.error(request,
                           "Your offer needs to be higher than the current bid")
            return False

def bid_email(request, artifact, new_bid):
    auction = get_object_or_404(Auction, artifact=artifact)
    email_title = 'Artifact Auctions - '+artifact.name
    email_message = 'You have been outbid on '+artifact.name+'. The current bid is now £'+str(new_bid)+'.'
    bids = Bid.objects.filter(auction=auction)
    try:
        current_bidder = bids.order_by('-bid_amount')[0].bidder
    except:
        current_bidder = None
    if current_bidder:
        send_mail(
        email_title,
        email_message,
        'admin@artifact-auction.com',
        [current_bidder.email],
        fail_silently=False,)      
        
"""return current bid value on artifact"""
def get_bid(request):
    if request.method == "GET":
        id = request.GET["artifact_id"]
        artifact = get_object_or_404(Artifact, pk=id)
        response_data = {}
        if artifact.sold is False:
            try:
                auction = get_object_or_404(Auction, artifact=artifact)
                bids = Bid.objects.filter(auction=auction)
                try:
                    current_bid = bids.order_by('-bid_amount')[0].bid_amount               
                except:
                    current_bid = 0
                """no need to pass reserve price - if bid is higher then page will reload which will update the reserve price"""
                response_data['in_auction'] = True
                response_data['current_bid'] = float(current_bid)
                response_data['start_time'] = str(auction.start_date)
                response_data['end_time'] = str(auction.end_date)
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except:
                response_data['message']=artifact.name+': Not yet listed for auction.'
                response = HttpResponse(json.dumps(response_data), content_type="application/json")
                return response
        else: 
            response_data['message']=artifact.name+' has already sold, no auction information'
            response = HttpResponse(json.dumps(response_data), content_type="application/json")            
            return response