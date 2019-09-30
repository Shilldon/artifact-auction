from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    remain_anonymous = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print("created user")
    print("sender:", sender)
    print("instance:", instance)
    print("created:", created)
    print("sender:", sender)
    if created:
        Profile.objects.create(user=instance)
        print("PRofile", Profile(instance))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("sender:", sender)
    print("instance:", instance)
    print("saved user")
    instance.profile.save()