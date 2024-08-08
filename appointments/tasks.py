# appointments/tasks.py
from django.utils import timezone
from django.core.mail import send_mail
from .models import Appointment
from messaging.helpers import send_notification
from celery import shared_task
from django.urls import reverse

@shared_task
def send_appointment_reminders():
    now = timezone.now()
    reminder_time = now + timezone.timedelta(hours=4)
    appointments = Appointment.objects.filter(start_time__lte=reminder_time, start_time__gte=now, reminder_sent=False)

    for appointment in appointments:
        patient = appointment.patient
        doctor = appointment.doctor

        # Send notification to patient
        send_notification(
            user=patient,
            content=f'Reminder: You have an appointment with Dr. {doctor.get_full_name()} at {appointment.start_time}',
            icon='fa-calendar-alt',
            link=reverse('appointment_detail', args=[appointment.pk]),
            link_name='View Appointment'
        )

        # Send notification to doctor
        send_notification(
            user=doctor,
            content=f'Reminder: You have an appointment with {patient.get_full_name()} at {appointment.start_time}',
            icon='fa-calendar-alt',
            link=reverse('appointment_detail', args=[appointment.pk]),
            link_name='View Appointment'
        )

        # Mark reminder as sent
        appointment.reminder_sent = True
        appointment.save()
