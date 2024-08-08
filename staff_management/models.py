from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.conf import settings

class Shift(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    shift_start_time = models.TimeField()
    shift_stop_time = models.TimeField()
    shift_type = models.CharField(max_length=50, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('night', 'Night')])
    days_of_week = models.CharField(max_length=50, choices=[('monday_to_friday', 'Monday to Friday'), ('saturday_and_sunday', 'Saturday and Sunday')])
    break_start_time = models.TimeField(blank=True, null=True)
    break_stop_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def shift_duration(self):
        # Calculate shift duration in hours
        shift_start = self.shift_start_time
        shift_stop = self.shift_stop_time
        duration = (shift_stop.hour - shift_start.hour) + (shift_stop.minute - shift_start.minute) / 60
        return duration

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='department_head')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    SHIFT_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('overtime', 'Overtime'),
        ('on_call', 'On Call'),
    ]
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'High'),
        (4, 'Urgent'),
    ]

    employee = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE)
    shift = models.ForeignKey('Shift', null=True, on_delete=models.DO_NOTHING) 
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_schedules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    break_duration = models.DurationField(default=timedelta(minutes=30))
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.shift.shift_start_time.strftime('%Y-%m-%d %H:%M')} to {self.shift.shift_end_time.strftime('%Y-%m-%d %H:%M')}"

    def get_shift_duration(self):
        return self.shift_end_time - self.shift_start_time

    class Meta:
        ordering = ['shift__shift_start_time', 'employee']


class NoticeBoard(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=[('announcement', 'Announcement'), ('event', 'Event'), ('news', 'News')])
    tags = models.CharField(max_length=255, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def is_expired(self):
        """Check if the notice has expired."""
        return self.expires_on and self.expires_on < timezone.now()

    # def get_absolute_url(self):
    #     """Return the URL for the notice detail view."""
    #     # return reverse('notice-detail', args=[()])

    def send_notification(self):
        """Send notifications to users when a new notice is posted."""
        # Implement notification logic here
        pass


class StaffOnDuty(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, null=True, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('on_leave', 'On Leave')])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    break_start = models.TimeField(blank=True, null=True)
    break_end = models.TimeField(blank=True, null=True)
    overtime = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.date} ({self.shift_start} to {self.shift_end})"
