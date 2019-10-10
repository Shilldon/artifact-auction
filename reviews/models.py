from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from artifacts.models import Artifact

class Review(models.Model):
    description = models.CharField(max_length=400, blank=True, default="")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.artifact.name
    