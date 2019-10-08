from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from artifacts.models import Artifact


class Auction(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20, default='Artifact Name')
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    current_bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    reserve_price = models.DecimalField(max_digits=11, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def clean(self):
        if self.end_date is not None and self.start_date is not None and self.end_date < self.start_date:
            raise ValidationError('Auction end date must be after start date.')
        if self.end_date is not None and self.start_date is None:
            raise ValidationError('Enter start date or remove auction end date.')
        if self.artifact.sold is True:
            self.artifact = None
    
    def __str__(self):
        return self.artifact.name+" Auction"

@receiver(post_save, sender=Auction)
def change_auction(sender, instance, **kwargs):
    if instance.start_date is not None:
        instance.artifact.in_auction = True
    else:
        instance.artifact.in_auction = False
    instance.artifact.save()       
    
@receiver(post_delete, sender=Auction)
def add_auction(sender, instance, **kwargs):
    instance.artifact.in_auction = False
    instance.artifact.save()