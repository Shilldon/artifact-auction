from django.shortcuts import render, get_object_or_404, redirect
from bids.models import Bid

def get_bidder(request, auction):

    """
    REturn the name of the highest bidder in the auction. If the highest
    bidder has chosen to remain anonymous return "Anonymous"
    """
    bidder_name = None

    if auction is not None:
        bids = Bid.objects.filter(auction=auction)
        try:
            current_bidder = bids.order_by('-bid_amount')[0].bidder
        except:
            current_bidder = None
        if current_bidder is not None:
            bidder_name = current_bidder
            if current_bidder != request.user:
                if current_bidder.profile.remain_anonymous is True:
                    bidder_name = "Anonymous"

    return bidder_name