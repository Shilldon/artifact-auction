from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template.defaulttags import register
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.utils import timezone
from .models import Artifact
from auctions.models import Auction
from auctions.views import get_bidder
from bid.forms import BiddingForm
from bid.views import check_bid
from bid.models import Bids
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
    if request.method == "POST":
        search_form = SearchArtifactsForm(request.POST)
        artifacts_list = search_artifacts(request, search_form)
    else:
        search_form = SearchArtifactsForm()
        artifacts_list = cache.get('sorted_list')
        if not artifacts_list:
            artifacts_list = Artifact.objects.all()
 
    if index_search:
        auctions = Auction.objects.filter(end_date__gte=timezone.now())
        artifacts_list = Artifact.objects.filter(id__in=auctions.values('artifact'))        
 
    results = artifacts_list.count()
    page = request.GET.get('page', 1)

    paginator = Paginator(artifacts_list, 10)
    try:
        artifacts = paginator.page(page)
    except PageNotAnInteger:
        artifacts = paginator.page(1)
    except EmptyPage:
        artifacts = paginator.page(paginator.num_pages)
 
    """get the highest bid for each artifact displayed"""
    auctions = Auction.objects.all()
    auction_bids = {}
    for auction in auctions:
        bids = Bids.objects.filter(auction=auction)
        if bids:
            auction_bids[auction.artifact] = str(bids.order_by('-bid_amount')[0].bid_amount)
        else:
            auction_bids[auction.artifact] = 0 
    return render(request, "artifacts.html", {"artifacts_list": artifacts, "auctions" : auctions, "search_form" : search_form, "auction_bids" : auction_bids, "results": results})

""" Display a single artifact """
def display_artifact(request, id):
    artifact = get_object_or_404(Artifact, pk=id)
    events = Event.objects.filter(artifact=artifact).order_by('sort_year', 'month', 'day')
    historical_figures = Historical_Figure.objects.filter(artifact_possessed=artifact)

    try:
        auction = get_object_or_404(Auction, artifact=artifact)
        """Check if the artifact is in a current auction and return the name of the bidder"""
        bids = Bids.objects.filter(auction=auction)
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
    
    if request.method == "POST":
        bid_form = BiddingForm(request.POST)
        successful_bid=check_bid(request, bid_form, artifact)
    else:
        bid_form = BiddingForm()
        successful_bid=False
    
    try:
        review = get_object_or_404(Review, artifact=artifact)
        rating = range(review.rating)
    except:
        review = None
        rating = range(0)
    
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
            
