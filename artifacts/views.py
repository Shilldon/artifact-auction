from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.utils import timezone
from .models import Artifact
from auctions.models import Auction, Bid
from auctions.views import get_bidder, check_bid
from auctions.forms import BiddingForm
from history.models import Event, Historical_Figure
from reviews.models import Review
from search.forms import SearchArtifactsForm
from search.views import search_artifacts

from django.core.mail import send_mail

# Create your views here.

""" filter to return value from dictionary in template"""
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

""" Display list of all artifacts """
def artifacts_list(request, index_search):
    """
    Create a list of artifacts to display on the page.
    First call on the cache to check if a the artifacts have been filtered 
    from a previous search. If not return list of all artifacts,
    """
    artifacts_list = cache.get('sorted_list')
    if request.method == "POST":
        search_form = SearchArtifactsForm(request.POST)
        if search_form.is_valid():
            artifacts_list = search_artifacts(request, search_form)
        if artifacts_list is None:
            artifacts_list = Artifact.objects.all()
    else:
        search_form = SearchArtifactsForm()
        artifacts_list = cache.get('sorted_list')
        if artifacts_list is None:
            artifacts_list = Artifact.objects.all()
 
    """
    On rendering the index page return a list of artifacts in current auctions
    to display links to those auctions.
    """
    if index_search:
        auctions = Auction.objects.filter(end_date__gte=timezone.now())
        artifacts_list = Artifact.objects.filter(id__in=auctions
                                                 .values('artifact'))        
 
    """
    Pagination for lists of artifacts greater than 10 results. Count total 
    results to display at head of page.
    """
    results = artifacts_list.count()
    page = request.GET.get('page', 1)

    paginator = Paginator(artifacts_list, 10)
    try:
        artifacts = paginator.page(page)
    except PageNotAnInteger:
        artifacts = paginator.page(1)
    except EmptyPage:
        artifacts = paginator.page(paginator.num_pages)
 
    """
    Get queryset of all auctions for templae to display information for each 
    artifact in an auction.
    """
    auctions = Auction.objects.all()
    auction_bids = {}
    """
    Create a list of the highest bids for each artifact to display in the 
    template auction status section for each artifact.
    """
    for auction in auctions:
        bids = Bid.objects.filter(auction=auction)
        if bids:
            auction_bids[auction.artifact] = bids.order_by('-bid_amount')[0]\
                                                           .bid_amount
        else:
            auction_bids[auction.artifact] = 0 
    return render(request, "artifacts.html", {
                                              "artifacts_list": artifacts, 
                                              "auctions" : auctions, 
                                              "search_form" : search_form, 
                                              "auction_bids" : auction_bids, 
                                              "results": results
                                            })

""" Display a single artifact """
def display_artifact(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    """
    Get querysets of events and historical_figures associated with the 
    artifact to pass to template.
    Ensure queryset of events is sorted by date.
    """
    events = Event.objects.filter(artifact=artifact).order_by('sort_year', 
                                                              'month', 'day')
    historical_figures = Historical_Figure.objects\
                                          .filter(artifact_possessed=artifact)

    try:
        auction = get_object_or_404(Auction, artifact=artifact)
        """
        Check if the artifact is in a current auction and, if so, return the 
        name of the highest bidder to display in the template.
        """
        bids = Bid.objects.filter(auction=auction)
        if bids:
            bidder_name = get_bidder(request, auction)
            current_bid = bids.order_by('-bid_amount')[0].bid_amount
            current_bidder = bids.order_by('-bid_amount')[0].bidder
        else:
            bidder_name = ""
            current_bid = 0
            current_bidder = None
    except:
        auction = None
        bids = {}
        bidder_name = ""
        current_bid = 0
        current_bidder = None
    
    """
    Bidding form is rendered in template. If form post bid information check if
    the bid is higher than the current highest bid otherwise render the 
    blank bidding form to the template.
    """
    if request.method == "POST":
        bid_form = BiddingForm(request.POST)
        successful_bid=check_bid(request, bid_form, artifact)
    else:
        bid_form = BiddingForm()
        successful_bid=False
    
    """
    Check if there are any reviews for the artifact, if not pass empty
    arguments
    """
    try:
        review = get_object_or_404(Review, artifact=artifact)
        rating = range(review.rating)
    except:
        review = None
        rating = range(0)
    
    """
    If the user has placed a bid that is successful, return to the page
    with a message that the bid was successful. Otherwise render the page
    fresh.
    """
    if successful_bid:
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request,"display_artifact.html", {
                    'artifact' : artifact, 
                    'auction' : auction, 
                    'bid_form' : bid_form, 
                    'bidder_name' : bidder_name, 
                    'bids' : bids, 
                    'current_bid' : current_bid,
                    'current_bidder' : current_bidder,
                    'review' : review,
                    'rating' : rating,
                    'events' : events,
                    'historical_figures' : historical_figures
        })