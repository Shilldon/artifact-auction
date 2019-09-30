from django.shortcuts import render, get_object_or_404, redirect
from .models import Artifact
from bid.forms import BiddingForm
from bid.views import place_bid, check_bid

# Create your views here.
""" Display list of all artifacts """
def artifacts_list(request):
    artifacts = Artifact.objects.all()
    return render(request, "artifacts.html", {"artifacts_list": artifacts})

""" Display a single artifact """
def display_artifact(request, id):

    artifact = get_object_or_404(Artifact, pk=id)
    bid_form = place_bid(request)

    """ Get the user who is currently the highest bidder, to display name as the
    highest bidder for the artifact"""
    current_bidder = artifact.current_bidder
    if current_bidder:
        bidder_name = current_bidder
        if current_bidder != request.user:
            if current_bidder.profile.remain_anonymous is True:
                bidder_name = "Anonymous"
    else:
        bidder_name = None
    successful_bid = check_bid(request, bid_form, artifact)
    if successful_bid:
        return redirect('artifacts_list')
    else:    
        return render(request,"display_artifact.html", {'artifact' : artifact, 'bid_form' : bid_form, 'bidder_name' : bidder_name})
