from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from artifacts.models import Artifact
from auctions.models import Auction, Bid


@login_required()
def view_collection(request):
    """
    A view that renders the contents of the user's collection to the page
    """

    """
    First create a list of all artifacts won but not paid for by the user.
    Look up all finished auctions and find the highest bidder in each. If the
    highest bidder is the user add the artifact to the list
    """
    auctions = Auction.objects.filter(end_date__lte=timezone.now())
    artifacts_won = {}
    total = 0
    for auction in auctions:
        bids = Bid.objects.filter(auction=auction)
        try:
            highest_bid = bids.order_by('-bid_amount')[0].bid_amount
            highest_bidder = bids.order_by('-bid_amount')[0].bidder
            if highest_bidder == request.user and \
                    highest_bid >= auction.artifact.reserve_price:
                """
                Add highest bid to the running total - this is the amount
                the user will have to pay if they click 'pay now'
                """
                total += highest_bid
                artifacts_won[auction.artifact.id] = \
                    {
                     'artifact': auction.artifact,
                     'bid': highest_bid
                     }
        except:
            None

    """
    Then find all artifacts owned by the user
    """
    artifacts_owned = Artifact.objects.filter(owner=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(artifacts_owned, 10)
    try:
        artifacts_owned_list = paginator.page(page)
    except PageNotAnInteger:
        artifacts_owned_list = paginator.page(1)
    except EmptyPage:
        artifacts_owned_list = paginator.page(paginator.num_pages)

    """
    Page displays two separate lists for the user.
    Artifacts won (but not paid for) and Artifacts owned
    """
    return render(request, "collection.html",
                  {
                   "artifacts_owned": artifacts_owned_list,
                   "artifacts_won": artifacts_won,
                   "total": total
                   }
                  )
