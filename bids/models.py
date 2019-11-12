from django.db import models
from django.contrib.auth.models import User
from auctions.models import Auction
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db.models import Max
from django.utils import timezone
from django.core.mail import send_mail
from decimal import Decimal

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(auto_now=False, null=True, blank=True)
    
    def __str__(self):
        return self.auction.artifact.name+": "+str(self.bid_amount)

@receiver(pre_delete, sender=Bid, dispatch_uid="bid_delete_signal")
def update_buy_now(sender, instance, using, **kwargs):
    """a check to, if the Bid has been deleted, make updates to the auction and
    buy_now_price"""
    
    auction = instance.auction
    try:
        bids = Bid.objects.filter(auction=auction)
        highest_bid = bids.order_by('-bid_amount')[0]
        if instance == highest_bid:
            """if the auction has come to an end delete the auction as the final
            winning bid has been withdrawn"""
            if auction.end_date < timezone.now():
                auction.delete()
                
            elif len(bids)>1:
                """otherwise find the next highest bid and set the buy_now_price 
                relative to the next highest bid and email the next_highest_bidder
                that they are back in the running"""
            
                next_bid = bids.order_by('bid_amount')[1].bid_amount
                next_bidder = bids.order_by('bid_amount')[1].bidder
                artifact = auction.artifact
                email_title = 'Artifact Auctions - Your bid on '+artifact.name
                email_message_bid = 'The highest bidder has withdrawn their \
                                    bid. You are back in the running as the \
                                    highest bidder on '+artifact.name+'.'
                send_mail(
                    email_title,
                    email_message_bid,
                    'admin@artifact-auction.com',
                    [next_bidder.email],
                    fail_silently=False,)  
                 
                """update the buy_now_price, if appropriate"""
                if next_bid>artifact.reserve_price:
                    artifact.buy_now_price = Decimal(next_bid) * Decimal(1.2)
                    artifact.save()
    except:
        None