from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now
from django.shortcuts import render
from artifacts.models import Artifact
from auctions.models import Auction


# Create your views here.
def index(request):
    
    auctions = Auction.objects.filter(start_date__lte=timezone.now(),end_date__gt=timezone.now())
    if auctions:
        if auctions.count()==1:
            auction_status="Current auction"
        else:
            auction_status="Current auctions"
    else:
        auction_status="No live auctions"
    
    return render(request, 'index.html', {"auctions" : auctions, "auction_status" : auction_status})
