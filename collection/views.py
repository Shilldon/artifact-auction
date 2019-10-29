from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils import timezone
from artifacts.models import Artifact
from auctions.models import Auction
from bid.models import Bids

def view_collection(request):
    """A view that renders the collection contents page"""
    collection = request.session.get('collection')
    
    auctions = Auction.objects.filter(end_date__lte=timezone.now())
    artifacts_won = {}
    total = 0
    for auction in auctions:
        bids = Bids.objects.filter(auction=auction)
        try:
            highest_bid = bids.order_by('-bid_amount')[0].bid_amount
            highest_bidder = bids.order_by('-bid_amount')[0].bidder
            if highest_bidder==request.user:
                total+=highest_bid
                artifacts_won[auction.artifact.id]={ 'artifact' : auction.artifact, 'bid' : highest_bid }
        except:
            None
    artifacts_owned = Artifact.objects.filter(owner=request.user)

    return render(request, "collection.html", { "artifacts_owned" : artifacts_owned, "artifacts_won" : artifacts_won, 'total' : total })


