from django.db import models
from django.contrib.auth.models import User
from auctions.models import Auction
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(auto_now=False, null=True, blank=True)
    
    def __str__(self):
        return self.auction.artifact.name+": "+str(self.bid_amount)
    