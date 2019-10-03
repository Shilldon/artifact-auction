from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=200, default='')
    
    def __str__(self):
        return self.name

class Artifact(models.Model):
    TYPE_CHOICES = [
        ('CULTURAL', "Cultural"), 
        ('MEDIA', "Media"),
        ('KNOWLEDGE', "Knowledge"),
        ('DATA', "Data")
    ]
    
    name = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=500, default='An artifact')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    reserve_price = models.DecimalField(max_digits=11, decimal_places=2, default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0) #the buy now price or maximum bid price
    current_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="artifact_bidder")
    reserved = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="artifact_owner")
    listed_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    auction_end_date = models.DateTimeField(null=True, blank=True)
    # purchase_date = models.DateTimeField(null=True, blank=True)
    
    def date_listed(self):
        try:
            return self.listed_date.strftime('%b %d, %Y %H:%M:%S')
        except:
            return None
    
    def date_auction_end(self):
        try:
            return self.auction_end_date.strftime('%b %d, %Y %H:%M:%S')
        except:
            return None
   
    def clean(self):
        if self.owner == None and self.sold == True:
            raise ValidationError('No owner, set sold to false or set owner.')
        if self.sold == False and self.owner is not None:
            raise ValidationError('Marked as sold, set owner to none or mark as sold.')
        if self.sold == True and self.current_bidder is not None:
            raise ValidationError('Artifact marked as sold, set current bidder to none or set sold as false.')
        if self.sold == True and self.reserved is True:
            raise ValidationError('Artifact marked as sold and reserved, set either to false.')
            
        if self.current_bidder is None and self.reserved is True:
            raise ValidationError('No current bidder, set reserved to false or set current bidder.')
        if self.current_bidder is None and self.bid > 0:
            raise ValidationError('No current bidder, set bid to 0 or set bid.')
        if self.current_bidder is not None and self.bid == 0:
            raise ValidationError('Current bidder set, set bid value greater than 0.')
        if self.current_bidder is not None and self.owner is not None:
            raise ValidationError('Error: owner and current bidder cannot both contain values. Set one to none.')
        
            
        if self.reserved == True and self.owner is not None:
            raise ValidationError('Artifact marked as reserved, set owner to none.')

        if self.auction_end_date is not None and self.listed_date is not None and self.auction_end_date < self.listed_date:
            raise ValidationError('Auction end date must be after listed date.')
        if self.auction_end_date is not None and self.listed_date is None:
            raise ValidationError('Enter listing date or remove auction end date.')
 
   
    def __str__(self):
        return self.name

@receiver(post_delete, sender=User)
def delete_bids(sender, instance, **kwargs):
    print("user deleted")

