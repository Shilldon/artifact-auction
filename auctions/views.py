from django.shortcuts import render, get_object_or_404, redirect
from .models import Auction

def get_bidder(request, auction):

    bidder_name = None

    if auction is not None:
        current_bidder = auction.current_bidder
        if current_bidder is not None:
            bidder_name = current_bidder
            if current_bidder != request.user:
                if current_bidder.profile.remain_anonymous is True:
                    bidder_name = "Anonymous"

    return bidder_name