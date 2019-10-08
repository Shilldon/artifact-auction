from django.shortcuts import render, get_object_or_404, redirect
from .models import Artifact
from auctions.models import Auction
from auctions.views import get_bidder
from bid.forms import BiddingForm
from bid.views import check_bid
from bid.models import Bids
from reviews.models import Review

# Create your views here.
""" Display list of all artifacts """
def artifacts_list(request):
    artifacts = Artifact.objects.all()
    auctions = Auction.objects.all()
    return render(request, "artifacts.html", {"artifacts_list": artifacts, "auctions" : auctions})

""" Display a single artifact """
def display_artifact(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    try:
        auction = get_object_or_404(Auction, artifact=artifact)
        """Check if the artifact is in a current auction and return the name of the bidder"""
        bidder_name = get_bidder(request, auction)
        bids = Bids.objects.filter(auction=auction)
        print(bids)
    except:
        auction = None
        bids = {}
        bidder_name = ""
    
    if request.method == "POST":
        bid_form = BiddingForm(request.POST)
        successful_bid=check_bid(request, bid_form, artifact)
    else:
        bid_form = BiddingForm()
    
    try:
        review = get_object_or_404(Review, artifact=artifact)
    except:
        review = None
    
    try:
        if successful_bid:
            return redirect(artifacts_list)
    except:
        return render(request,"display_artifact.html", {'artifact' : artifact, 'auction' : auction, 'bid_form' : bid_form, 'bidder_name' : bidder_name, 'bids' : bids, 'review' : review })
            

