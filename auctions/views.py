import json
import datetime
from decimal import Decimal
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Auction, Bid
from artifacts.models import Artifact


def get_bidder(request, auction):
    """
    A view to return the name of the highest bidder in the auction.

    Find highest bidder from the bid objects associated with the particular
    auction. If the highest bidder has chosen to remain anonymous return
    "Anonymous"
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


def check_bid(request, bid_form, artifact):
    """
    A view to check the bid posted by the user.
    Take a bid from the user and check if higher than current bid
    """

    auction = get_object_or_404(Auction, artifact=artifact)

    if bid_form.is_valid():
        new_bid = Decimal(request.POST['amount_bid'])
        bids = Bid.objects.filter(auction=auction)
        try:
            current_bid = bids.order_by('-bid_amount')[0].bid_amount
        except:
            current_bid = 0
        if new_bid > current_bid:
            """
            Send email to previous bidder to inform them they have been outbid
            """
            bid_email(request, artifact, new_bid)
            bid = Bid(bid_amount=new_bid, bidder=request.user, auction=auction)
            bid.time = datetime.datetime.now()
            bid.save()

            if new_bid > artifact.buy_now_price and \
                new_bid > artifact.reserve_price:
                artifact.buy_now_price = Decimal(new_bid) * Decimal(1.2)
                artifact.save()

            messages.success(request,
                             "Thank you for your bid on %s. You will be "
                             "notified by email if you are outbid." %
                             (artifact.name))
            return True

        else:
            messages.error(request,
                           "Your offer needs to be higher than the current \
                           bid")
            return False


def bid_email(request, artifact, new_bid):
    """
    A view to email the previous highest bidder
    """
    auction = get_object_or_404(Auction, artifact=artifact)
    email_title = 'Artifact Auctions - '+artifact.name
    email_message = 'You have been outbid on ' + artifact.name + \
                    '. The current bid is now £' + str(new_bid) + '.'
    bids = Bid.objects.filter(auction=auction)
    try:
        current_bidder = bids.order_by('-bid_amount')[0].bidder
    except:
        current_bidder = None
    if current_bidder:
        send_mail(
                  email_title,
                  email_message,
                  'admin@artifact-auction.com',
                  [current_bidder.email],
                  fail_silently=False,)


def get_bid(request):
    """
    A view to get the highest bid and associated information on the particular
    artifact.

    This view returns value and associated information on ajax query to display
    on artifact list display artifact templates
    """
    if request.method == "GET":
        id = request.GET["artifact_id"]
        artifact = get_object_or_404(Artifact, pk=id)
        response_data = {}
        if artifact.sold is False:
            try:
                auction = get_object_or_404(Auction, artifact=artifact)
                bids = Bid.objects.filter(auction=auction)
                try:
                    current_bid = bids.order_by('-bid_amount')[0].bid_amount
                except:
                    current_bid = 0
                response_data['in_auction'] = True
                response_data['current_bid'] = float(current_bid)
                response_data['start_time'] = str(auction.start_date)
                response_data['end_time'] = str(auction.end_date)
                return HttpResponse(
                                    json.dumps(response_data),
                                    content_type="application/json"
                                    )
            except:
                response_data['message'] = artifact.name + \
                                         ': Not yet listed for auction.'
                response = HttpResponse(
                                        json.dumps(response_data),
                                        content_type="application/json"
                                        )
                return response
        else:
            response_data['message'] = artifact.name + \
                                    ' has already sold, no auction information'
            response = HttpResponse(
                                    json.dumps(response_data),
                                    content_type="application/json"
                                    )
            return response
