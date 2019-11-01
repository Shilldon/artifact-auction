from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    remain_anonymous = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='images', null=True, blank=True)
    description = models.TextField(default='Artifact collector', null=True, blank=True)
    
    def __str__(self):
        return "%s's profile" % self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()