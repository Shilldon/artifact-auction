from django.db import models
from django.core.exceptions import ValidationError
from artifacts.models import Artifact

class Owner(models.Model):
    name = models.CharField(max_length=30, default="")
    description = models.CharField(max_length=800, default="")
    
    def __str__(self):
        return self.name    

class Event(models.Model):
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=800, default="")
    year = models.PositiveIntegerField(default=0)
    bc = models.CharField(max_length=2, default="AD")
    month = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    day = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None) 
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, default=None, blank=True, null=True)

    def clean(self):
        day =self.day
        month = self.month
        if month is None and day: 
            raise ValidationError(
                "Enter day of the month."
                )
        if month in [4, 6, 9, 11] and day > 30:
            raise ValidationError(
                "Day must be less than 31."
                )            
        if month == 2 and day > 29:
            raise ValidationError(
                "Day must be less than 30."
                )   

    def __str__(self):
        return self.name    
    
    