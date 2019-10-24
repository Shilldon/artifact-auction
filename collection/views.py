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
    for auction in auctions:
        bids = Bids.objects.filter(auction=auction)
        highest_bid = bids.order_by('-bid_amount')[0].bid_amount
        highest_bidder = bids.order_by('-bid_amount')[0].bidder
        if highest_bidder==request.user:
            artifacts_won[auction.artifact.id]={ 'artifact' : auction.artifact, 'bid' : highest_bid }
    
    artifacts_owned = Artifact.objects.filter(owner=request.user)

    return render(request, "collection.html", { "artifacts_owned" : artifacts_owned, "artifacts_won" : artifacts_won })

def add_to_collection(request, id, buy_now):
    """
    Get the user's collection of artifacts and, if not already in the collection 
    add the selected artifact to the collection
    """
    collection = request.session.get('collection', {})
    artifact = get_object_or_404(Artifact, pk=id)
    
    auction = get_object_or_404(Auction, artifact=artifact)
    last_bid = Bids.objects.filter(auction=auction).order_by('-bid_amount')[0].bid_amount
    
    if int(buy_now)==1:
        price = artifact.buy_now_price
    else:
        price = float(last_bid)
    
    if id not in collection:
        collection[id] = collection.get(id, price)
        request.session['collection'] = collection

    return redirect(reverse('checkout'))