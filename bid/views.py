from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
#from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from .forms import BiddingForm
from artifacts.models import Artifact
from decimal import Decimal

""" Take a bid from the user and check if higher than current bid """
def place_bid(request):
    if request.method=="POST":
        bid_form = BiddingForm(request.POST)
    else:
        bid_form = BiddingForm()
    
    return bid_form
    
def check_bid(request, bid_form, artifact):
    successful_bid = False
    if bid_form.is_valid():
        new_bid = Decimal(request.POST['amount_bid'])
        current_bid = Decimal(artifact.bid)
        if new_bid > current_bid:
            artifact.bid = new_bid
            artifact.save()
            messages.success(request, 
                             "You have successfully placed your bid on %s" %artifact.name)
            successful_bid = True
        else:
            messages.error(request,
                           "Your offer needs to be higher than the current bid")
    return successful_bid    
    
