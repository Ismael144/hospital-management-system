from django.db import models
from appointments.models import Appointment
from django.conf import settings 

class LabTest(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), 
                      ('Completed', 'Completed'), 
                      ('Cancelled', 'Cancelled')]
    
    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    test_code = models.CharField(max_length=100, unique=True)
    date_collected = models.DateTimeField(auto_now_add=True)
    date_reported = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    results = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lab Test {self.test_name} for {self.patient}"

    def complete_test(self, results):
        """Mark the test as completed and record results."""
        self.results = results
        self.status = 'Completed'
        self.date_reported = models.DateTimeField(auto_now=True)
        self.save()


class Specimen(models.Model):
    CONDITION_CHOICES = [('Good', 'Good'), 
                         ('Poor', 'Poor')]
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='specimens')
    specimen_type = models.CharField(max_length=100)
    collection_date = models.DateTimeField()
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Specimen for {self.lab_test} ({self.specimen_type})"
    

class LabEquipment(models.Model):
    CALIBRATION_STATUS_CHOICES = [('Calibrated', 'Calibrated'), ('Not Calibrated', 'Not Calibrated')]
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    date_purchased = models.DateField()
    last_maintenance_date = models.DateField()
    next_maintenance_due = models.DateField()
    calibration_status = models.CharField(max_length=100, choices=CALIBRATION_STATUS_CHOICES, default='Not Calibrated')

    def __str__(self):
        return f"Lab Equipment {self.name} ({self.serial_number})"

    def needs_maintenance(self):
        """Check if maintenance is overdue."""
        from datetime import date
        return self.next_maintenance_due < date.today()

class LabResult(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result = models.TextField()
    date_performed = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the laboratorist

    def __str__(self):
        return f"Result for {self.test.name} on {self.appointment}"
    

class LaboratoryInventory(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
