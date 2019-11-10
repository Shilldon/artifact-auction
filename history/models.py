import re
import calendar
from django.db import models
from django.core.exceptions import ValidationError
from artifacts.models import Artifact

class Historical_Figure(models.Model):
    artifact_possessed = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None) 
    name = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    url_description = models.TextField(default="", blank=True)
    picture = models.ImageField(upload_to='images', null=True, blank=True)

    def clean(self):
        try:
            """ review description and replace all references to the artifact name with a url link to the artifact """       
            artifact_name = re.compile(self.artifact_possessed.name, re.IGNORECASE)
            artifact_link_string=artifact_name.sub("<a href='/artifacts/artifact/"+str(self.artifact_possessed.id)+"'>"+self.artifact_possessed.name+"</a>", self.description)
            """review the amended description and replace all references to the artifact historical_figure with a url link to the historical_figure """
            self.url_description=artifact_link_string

        except:
            raise ValidationError(
                "Please enter the artifact associated with this person."
                )                

    def __str__(self):
        return self.name    

class Event(models.Model):
    
    BCAD_CHOICE = [
        ('BC', "BC"), 
        ('AD', "AD")
    ]
    
    name = models.CharField(max_length=50, default="")
    description = models.TextField(default="")
    url_description = models.TextField(default="", blank=True)
    year = models.PositiveIntegerField(default=0)
    sort_year = models.IntegerField(default=0)
    bc = models.CharField(max_length=2, choices=BCAD_CHOICE, default='BC')
    month = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    day = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None) 
    historical_figure = models.ForeignKey(Historical_Figure, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    picture = models.ImageField(upload_to='images', null=True, blank=True)
    date = models.CharField(max_length=25, blank=True)
    
    def clean(self):

        day = self.day
        month = self.month
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

        if self.month:
            month = calendar.month_name[self.month]

            
        if day or month or year:
            date = [day, month, year, self.bc]
            date_list = [str(i or '') for i in date]
            self.date = ' '.join(map(str, date_list)).lstrip()
        
        """ review description and replace all references to the artifact name with a url link to the artifact """
        try:
            artifact_name = re.compile(self.artifact.name, re.IGNORECASE)
            artifact_link_string=artifact_name.sub("<a href='/artifacts/artifact/"+str(self.artifact.id)+"'>"+self.artifact.name+"</a>", self.description)
            """review the amended description and replace all references to the artifact historical_figure with a url link to the historical_figure """
            if self.historical_figure:
                historical_figure_name = re.compile(self.historical_figure.name, re.IGNORECASE)
                self.url_description=historical_figure_name.sub("<a href='/history/historical_figure/"+str(self.historical_figure.id)+"'>"+self.historical_figure.name+"</a>", artifact_link_string)
            else:
                self.url_description=artifact_link_string
        except:
            raise ValidationError(
                "Please enter the artifact associated with this event."
                )  
            
    def __str__(self):
        return self.name    
    
    