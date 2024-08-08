from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from accounts.models import CaseManager

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_case_manager_profile(sender, instance, created, **kwargs):
    if created and instance.is_case_manager:  # Ensure this check matches your logic for identifying case managers
        CaseManager.objects.create(user=instance)
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_case_manager_profile(sender, instance, **kwargs):
    if hasattr(instance, 'case_manager_profile'):
        instance.case_manager_profile.save()
