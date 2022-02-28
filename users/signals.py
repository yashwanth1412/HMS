from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MyUser

@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        instance.is_security=True
        instance.save()
