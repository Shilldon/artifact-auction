import re
import calendar
from django.db import models
from django.core.exceptions import ValidationError
from artifacts.models import Artifact

class Owner(models.Model):
    name = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    picture = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.name    

class Event(models.Model):
    
    BCAD_CHOICE = [
        ('BC', "BC"), 
        ('AD', "AD")
    ]
    
    name = models.CharField(max_length=50, default="")
    description = models.TextField(default="")
    url_description = models.CharField(max_length=800, default="", blank=True)
    year = models.PositiveIntegerField(default=0)
    sort_year = models.IntegerField(default=0)
    bc = models.CharField(max_length=2, choices=BCAD_CHOICE, default='BC')
    month = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    day = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None) 
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    picture = models.ImageField(upload_to='images', null=True, blank=True)
    date = models.CharField(max_length=25, blank=True)
    
    def clean(self):
        
        day = self.day
        if self.month:
            month = calendar.month_name[self.month]
        else:
            month = None
        year = self.year
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
        if year!=0:
            if self.bc=="BC":
                self.sort_year=-year
            else:
                self.sort_year=year
            
        if day or month or year:
            date = [day, month, year, self.bc]
            date_list = [str(i or '') for i in date]
            self.date = ' '.join(map(str, date_list)).lstrip()
        
        """ review description and replace all references to the artifact name with a url link to the artifact """       
        artifact_name = re.compile(self.artifact.name, re.IGNORECASE)
        artifact_link_string=artifact_name.sub("<a href='/artifacts/artifact/"+str(self.artifact.id)+"'>"+self.artifact.name+"</a>", self.description)

        """review the amended description and replace all references to the artifact owner with a url link to the owner """
        if self.owner:
            owner_name = re.compile(self.owner.name, re.IGNORECASE)
            self.url_description=owner_name.sub("<a href='/history/historical_figure/"+str(self.owner.id)+"'>"+self.owner.name+"</a>", artifact_link_string)

    def __str__(self):
        return self.name    
    
    