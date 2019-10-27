import re
from django.db import models
from django.core.exceptions import ValidationError
from artifacts.models import Artifact

class Owner(models.Model):
    name = models.CharField(max_length=30, default="")
    description = models.CharField(max_length=800, default="")
    picture = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.name    

class Event(models.Model):
    
    BCAD_CHOICE = [
        ('BC', "BC"), 
        ('AD', "AD")
    ]
    
    
    name = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=800, default="")
    url_description = models.CharField(max_length=800, default="", blank=True)
    year = models.PositiveIntegerField(default=0)
    sort_year = models.IntegerField(default=0)
    bc = models.CharField(max_length=2, choices=BCAD_CHOICE, default='BC')
    month = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    day = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None) 
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    picture = models.ImageField(upload_to='images', null=True, blank=True)
    
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
        if self.year!=0:
            if self.bc=="BC":
                self.sort_year=-self.year
            else:
                self.sort_year=self.year
        artifact_name = re.compile(self.artifact.name, re.IGNORECASE)
        artifact_link_string=artifact_name.sub("<a href='/artifacts/artifact/"+str(self.artifact.id)+"'>"+self.artifact.name+"</a>", self.description)

        owner_name = re.compile(self.owner.name, re.IGNORECASE)
        self.url_description=owner_name.sub("<a href='/history/historical_figure/"+str(self.owner.id)+"'>"+self.owner.name+"</a>", artifact_link_string)

        
        
    def __str__(self):
        return self.name    
    
    