from django.db import models
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=200, default='')

class Artifact(models.Model):
    TYPE_CHOICES = [
        ('CULTURAL', "Cultural"), 
        ('MEDIA', "Media"),
        ('KNOWLEDGE', "Knowledge"),
        ('DATA', "Data")
    ]
    
    name = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, default='An artifact')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    reserve_price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    sold = models.BooleanField(default=False)
    current_bidder = models.ForeignKey(User, null=True, blank=True)
    # listed_date = models.DateTimeField()
    # purchase_date = models.DateTimeField(null=True, blank=True)

