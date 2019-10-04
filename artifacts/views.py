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
        #bid_form = place_bid(request)
        bid_form = BiddingForm(request.POST)
        check_bid(request, bid_form, artifact)
    else:
        bid_form = BiddingForm()
    
    return render(request,"display_artifact.html", {'artifact' : artifact, 'auction' : auction, 'bid_form' : bid_form, 'bidder_name' : bidder_name})
            
"""return current bid value on artifact"""
def get_bid(request):
    if request.method == "GET":
        id = request.GET["artifact_id"]
        artifact = get_object_or_404(Artifact, pk=id)
        auction = get_object_or_404(Auction, artifact=artifact)
        
        return HttpResponse(auction.current_bid)
    else:
        return HttpResponse("unsucessful")