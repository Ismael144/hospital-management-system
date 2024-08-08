from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Activity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    Activity.objects.create(user=user, action='login')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    Activity.objects.create(user=user, action='logout')
