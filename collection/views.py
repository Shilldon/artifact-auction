from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from artifacts.models import Artifact
from auctions.models import Auction
from bid.models import Bids

@login_required()
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

    page = request.GET.get('page', 1)

    paginator = Paginator(artifacts_owned, 10)
    try:
        artifacts_owned_list = paginator.page(page)
    except PageNotAnInteger:
        artifacts_owned_list = paginator.page(1)
    except EmptyPage:
        artifacts_owned_list = paginator.page(paginator.num_pages)

    return render(request, "collection.html", { "artifacts_owned" : artifacts_owned_list, "artifacts_won" : artifacts_won, 'total' : total })


