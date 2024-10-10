# medications/tasks.py

# This celery task checks whether a medication is approaching its expiry and notifies  

from datetime import date, timedelta
from celery import shared_task
from django.urls import reverse
from django.utils import timezone
from .models import Medication
from messaging.helpers import send_notification

@shared_task
def check_medication_expiry():
    """ Check if any medication is approaching its expiry date and send notifications. """
    today = date.today()
    warning_period = timedelta(days=30)  # Set the warning period (e.g., 30 days before expiry)
    
    medications = Medication.objects.filter(expiry_date__lte=today + warning_period, remainder_sent=False)
    
    for medication in medications:
        # Send notification to the relevant staff (e.g., pharmacists)
        send_notification(
            user=medication.dispensed_by,  # Assuming dispensed_by is a pharmacist or related user
            content=f'Medication "{medication.name}" is approaching its expiry date ({medication.expiry_date}).',
            icon='fa-exclamation-triangle',
            link=reverse('medication_detail', args=[medication.pk]),
            link_name='View Medication'
        )

        # Mark reminder as sent
        medication.reminder_sent = True
        medication.save()
