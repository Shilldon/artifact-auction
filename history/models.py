from django.db import models
from artifacts.models import Artifact

class Event(models.Model):
    name = models.CharField(max_length=30, required=True)
    description = models.CharField(max_length=800, required=True)
    year = models.PositiveIntegerField(required=False)
    month = models.PositiveSmallIntegerField(min_value=1, max_value=12, required=False)
    day = models.PositiveSmallIntegerField(min_value=1, max_value=31, required=False)
    artifact = models.ForeignKey(Artifact) 
    