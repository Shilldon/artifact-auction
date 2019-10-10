from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import register
from .models import Artifact
from auctions.models import Auction
from auctions.views import get_bidder
from bid.forms import BiddingForm
from bid.views import check_bid
from bid.models import Bids
from reviews.models import Review
from search.forms import SearchArtifactsForm
from search.views import search_artifacts

# Create your views here.

""" filter to return value from dictionary in template"""
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


""" Display list of all artifacts """
def artifacts_list(request):
    if request.method == "POST":
        search_form = SearchArtifactsForm(request.POST)
        artifacts = search_artifacts(request, search_form)
    else:
        search_form = SearchArtifactsForm()
        artifacts = Artifact.objects.all()
    auctions = Auction.objects.all()
    auction_bids = {}
    for auction in auctions:
        bids = Bids.objects.filter(auction=auction)
        auction_bids[auction.id]=str(bids.order_by('-bid_amount')[0].bid_amount)

    return render(request, "artifacts.html", {"artifacts_list": artifacts, "auctions" : auctions, "search_form" : search_form, "auction_bids" : auction_bids})

""" Display a single artifact """
def display_artifact(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    auction = get_object_or_404(Auction, artifact=artifact)
    if auction:
        auction = get_object_or_404(Auction, artifact=artifact)
        """Check if the artifact is in a current auction and return the name of the bidder"""
        bidder_name = get_bidder(request, auction)
        bids = Bids.objects.filter(auction=auction)
        current_bid = str(bids.order_by('-bid_amount')[0].bid_amount)
        current_bidder = bids.order_by('-bid_amount')[0].bidder
        print(current_bidder)
    else:
        auction = None
        bids = {}
        bidder_name = ""
        current_bid = 0
        current_bidder = None
    
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
        return render(request,"display_artifact.html", {
                    'artifact' : artifact, 
                    'auction' : auction, 
                    'bid_form' : bid_form, 
                    'bidder_name' : bidder_name, 
                    'bids' : bids, 
                    'current_bid' : current_bid,
                    'current_bidder' : current_bidder,
                    'review' : review 
        })
            

