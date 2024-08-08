from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import Laboratorist

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_laboratorist_profile(sender, instance, created, **kwargs):
    if created and instance.is_laboratorist:  # Ensure this check matches your logic for identifying laboratorists
        Laboratorist.objects.create(user=instance)
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_laboratorist_profile(sender, instance, **kwargs):
    if hasattr(instance, 'laboratorist_profile'):
        instance.laboratorist_profile.save()
