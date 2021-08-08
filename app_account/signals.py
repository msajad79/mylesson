from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User, dispatch_uid='uniqe_somthing')
def update_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
