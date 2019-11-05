from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from artifacts.models import Artifact


class Auction(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=20, default='Auction')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.end_date is not None and self.start_date is not None and self.end_date < self.start_date:
            raise ValidationError('Auction end date must be after start date.')
        if self.end_date is not None and self.start_date is None:
            raise ValidationError('Enter start date or remove auction end date.')
        if self.artifact.sold is True:
            raise ValidationError('That artifact has been sold.')
    
    def __str__(self):
        return self.artifact.name+" Auction"


