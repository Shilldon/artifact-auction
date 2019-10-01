from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

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
    reserve_price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0) #the buy now price or maximum bid price
    sold = models.BooleanField(default=False)
    current_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="artifact_bidder")
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="artifact_owner")
    listed_date = models.DateTimeField(default=timezone.now)
    auction_end_date = models.DateTimeField(null=True)
    # purchase_date = models.DateTimeField(null=True, blank=True)
    
    def date_listed(self):
        return self.listed_date.strftime('%b %d, %Y %H:%M:%S')
    
    def date_auction_end(self):
        return self.auction_end_date.strftime('%b %d, %Y %H:%M:%S')
   
    def __str__(self):
        return self.name

@receiver(post_delete, sender=User)
def delete_bids(sender, instance, **kwargs):
    print("user deleted")
