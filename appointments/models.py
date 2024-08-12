from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from messaging.models import Notification 
from django.utils import timezone

class Appointment(models.Model):
    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE, null=True, blank=True)
    nurse = models.ForeignKey("accounts.Nurse", on_delete=models.CASCADE, null=True, blank=True)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled')
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancellation_reason = models.TextField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        if self.doctor is None and self.nurse is None: 
            return "N/A"
        
        doctor_or_nurse = f"Dr. {self.doctor.employee.user.get_full_name()}" if self.nurse is None else f"Nr. {self.nurse.employee.user.get_full_name()}" 
        local_appointment_date = timezone.localtime(self.appointment_date)
        formatted_date = local_appointment_date.strftime('%A, %B %d, %Y at %I:%M %p')
        
        return f"Appt for {self.patient.user.first_name} {self.patient.user.last_name} with {doctor_or_nurse} On {formatted_date}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        
    def is_completed(self):
        return self.status == 'completed'

    def cancel(self):
        self.status = 'canceled'
        self.save()

    def start(self):
        self.status = 'ongoing'
        self.save()

    def complete(self):
        self.status = 'completed'
        self.save()
        
    def is_cancelled(self) -> bool: 
        return self.status.lower() == 'cancelled'


@receiver(post_save, sender=Appointment)
def appointment_created(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the doctor
        Notification.objects.create(
            user=instance.patient.user,
            content=f'New appointment created by {instance.patient.user.get_full_name()}.'
        )
        
        # Create a notification for the nurse if applicable
        if instance.nurse:
            Notification.objects.create(
                user=instance.nurse.employee.user,
                content=f'New appointment created by {instance.patient.user.get_full_name()}.'
            )
