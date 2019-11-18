from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
#from datetime import datetime
#from django.db.models import Max

from artifacts.models import Artifact

class Auction(models.Model):
    
    """
    Set Auction start date 2 minutes in the future as auction start date
    cannot be in the past. This should give time for the user to complete the 
    auction details. Default to 1 week long auction.
    """
    default_start_date = timezone.now() + timezone.timedelta(seconds=120)
    default_end_date = timezone.now() + timezone.timedelta(7)
    
    artifact = models.ForeignKey(Artifact, 
                                 on_delete=models.CASCADE, 
                                 default=None)
    name = models.CharField(max_length=20, default='Auction')
    start_date = models.DateTimeField(default=default_start_date)
    end_date = models.DateTimeField(default=default_end_date)

    def clean(self):
 
        """
        Check the user has entered valid start and end dates for the auction
        (end date must be after start date and start date not in the past)
        """
        if self.end_date < self.start_date:
            raise ValidationError('Auction end date must be after start date.')
            
        if self.start_date < timezone.now():
             raise ValidationError('The start date of the auction may not be in' 
                                   ' the past.')            
        
        """
        Check the user has not selected an artifact that has already sold.
        This validation should not be required as the auction form only enables
        the user to select unsold artifacts but is included as a double check
        """
        if self.artifact.sold is True:
            raise ValidationError('That artifact has been sold.')
            
    def __str__(self):
        return self.artifact.name+" Auction"

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(auto_now=False, null=True, blank=True)
    
    def __str__(self):
        return self.auction.artifact.name+": "+str(self.bid_amount)

@receiver(pre_delete, sender=Bid, dispatch_uid="bid_delete_signal")
def update_buy_now(sender, instance, using, **kwargs):
    """
    If admin deletes a bid, check to see if that was the highest bid, if so
    update the buy_now_price on the relevant artifact to reduce it to 20% 
    above the next highest bid (if the auction is still live and current_bidder
    bidding is over the reserve_price)
    """
    
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
                relative to the next highest bid and email the 
                next_highest_bidder that they are back in the running"""
            
                next_bid = bids.order_by('-bid_amount')[1].bid_amount
                next_bidder = bids.order_by('-bid_amount')[1].bidder
                artifact = auction.artifact
                if artifact.sold==False:
                    email_title = 'Artifact Auctions - \
                                  Your bid on '+artifact.name
                    email_message_bid = 'The highest bidder has withdrawn \
                                        their bid. You are back in the running\
                                         as the highest bidder \
                                        on '+artifact.name+'.'
                    send_mail(
                        email_title,
                        email_message_bid,
                        'admin@artifact-auction.com',
                        [next_bidder.email],
                        fail_silently=False,)  
                     
                    """update the buy_now_price, if appropriate"""
                    if next_bid>artifact.reserve_price:
                        artifact.buy_now_price = Decimal(next_bid) * \
                                                 Decimal(1.2)
                        artifact.save()
    except:
        None


