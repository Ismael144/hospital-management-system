import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django_ckeditor_5.fields import CKEditor5Field


def get_message_attachments(user_id: int, filename: str) -> str: 
    return f"{user_id}/{filename}"

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    content = CKEditor5Field('Content', config_name='extends')
    attachments = models.FileField(upload_to=get_message_attachments, null=True, blank=True)
    has_attachments = True if attachments else False
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"From {self.sender.get_full_name()} to {self.receiver.get_full_name()}"

    def get_attachment_url(self):
        if self.attachments:
            return self.attachments.url
        return None  # or return a default value

@receiver(post_delete, sender=Message)
def delete_attachments(sender, instance, **kwargs):
    if instance.attachments:
        if os.path.isfile(instance.attachments.path):
            os.remove(instance.attachments.path)
            

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=255, default='fa-bell')  # FontAwesome icon class
    link = models.URLField(null=True, blank=True)  # Optional link for the notification
    bg_color = models.CharField(max_length=20, default='#f8f9fa')  # Default light background color
    link_name = models.CharField(max_length=255, null=True, blank=True) # Name for the link

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.content
