from django.db import models
#from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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


