from django.db import models
from django.conf import settings 

class SystemLog(models.Model):
    EVENT_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    ]

    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.event_type} - {self.timestamp}'