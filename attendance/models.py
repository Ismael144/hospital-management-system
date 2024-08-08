from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Attendance(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('patient', 'Patient'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent')], default='present')

    def __str__(self):
        return f'{self.user.email} - {self.date} - {self.get_status_display()}'
