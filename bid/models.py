from django.db import models
from django.contrib.auth.models import User
from artifacts.models import Artifact
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Bids(models.Model):
    bid_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, blank=True, null=True)
    
"""
@receiver(post_delete, sender=User)
def delete_user_bids(sender, instance, **kwargs):
    print(instance.id)
    Bids.objects.filter(bidder=instance).delete()
    
    then update auction.current_bidder and current_bid with highest bid
    
    also do on save version for auction in case admin adjusts bidder and amount_bid
    
    ??instead hide bidder and amount from admin panel or make uneditable?
    At least give warning
    
"""