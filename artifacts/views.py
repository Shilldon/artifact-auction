import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Artifact
from auctions.models import Auction
from auctions.views import get_bidder
from bid.forms import BiddingForm
from bid.views import check_bid
from bid.models import Bids

# Create your views here.
""" Display list of all artifacts """
def artifacts_list(request):
    artifacts = Artifact.objects.all()
    bids = Bids.objects.all()
    return render(request, "artifacts.html", {"artifacts_list": artifacts, "bids" : bids})

""" Display a single artifact """
def display_artifact(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    auction = get_object_or_404(Auction, artifact=artifact)
    """Check if the artifact is in a current auction and return the name of the bidder"""
    bidder_name = get_bidder(request, auction)
    
    if request.method == "POST":
        bid_form = BiddingForm(request.POST)
        successful_bid=check_bid(request, bid_form, artifact)
    else:
        bid_form = BiddingForm()
    
    try:
        if successful_bid:
            return redirect(artifacts_list)
    except:
        return render(request,"display_artifact.html", {'artifact' : artifact, 'auction' : auction, 'bid_form' : bid_form, 'bidder_name' : bidder_name})
            
"""return current bid value on artifact"""
def get_bid(request):
    if request.method == "GET":
        id = request.GET["artifact_id"]
        artifact = get_object_or_404(Artifact, pk=id)
        auction = get_object_or_404(Auction, artifact=artifact)
        
        response_data = {}
        response_data['reserve_price'] = float(auction.reserve_price)
        response_data['current_bid'] = float(auction.current_bid)
        response_data['start_time'] = str(auction.start_date)
        response_data['end_time'] = str(auction.end_date)
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse("unsucessful")