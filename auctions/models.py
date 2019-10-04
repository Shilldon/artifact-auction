from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from artifacts.models import Artifact


class Auction(models.Model):
    name = models.CharField(max_length=20, default='Artifact Name')
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    current_bid = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    reserve_price = models.DecimalField(max_digits=11, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, blank=True, null=True)

    def reformatted_start_date(self):
        try:
            return self.start_date.strftime('%b %d, %Y %H:%M:%S')
        except:
            return None
    
    def reformatted_end_date(self):
        try:
            return self.end_date.strftime('%b %d, %Y %H:%M:%S')
        except:
            return None   
            
    def clean(self):
        if self.end_date is not None and self.start_date is not None and self.end_date < self.start_date:
            raise ValidationError('Auction end date must be after start date.')
        if self.end_date is not None and self.start_date is None:
            raise ValidationError('Enter start date or remove auction end date.')
    
    def __str__(self):
        return self.artifact.name
