from django.db import models
from django.conf import settings 
from django.core.exceptions import ValidationError
from datetime import date
from accounts.models import Patient

class Medication(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    dosage = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    batch_number = models.CharField(max_length=100, unique=True)
    expiry_date = models.DateField()
    reminder_sent = models.BooleanField(default=False)
   
    def __str__(self):
        return self.name

    def is_expired(self):
        """Check if the medication is expired."""
        return self.expiry_date < date.today()

    def adjust_stock(self, quantity):
        """Adjust stock quantity and ensure it does not fall below zero."""
        self.stock_quantity = max(self.stock_quantity + quantity, 0)
        self.save()

    def clean(self):
        """Custom validation for the model fields."""
        # Ensure expiry date is not in the past when adding a new medication
        if self.expiry_date < date.today():
            raise ValidationError("Expiry date cannot be in the past.")

        # Ensure price is not negative
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def save(self, *args, **kwargs):
        """Override save method to include validation checks."""
        self.clean()  # Call the clean method to validate fields
        super().save(*args, **kwargs)
        

class MedicationAssignment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medication)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    prescribing_doctor = models.ForeignKey('accounts.Doctor', null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.medication.name}"

    class Meta:
        unique_together = ['patient', 'start_date']
        

class Prescription(models.Model):
    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    medication = models.ManyToManyField(Medication)
    issue_date = models.DateTimeField(auto_now_add=True)
    instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Active')
    history = models.TextField(blank=True, null=True)  # History of status changes

    def __str__(self):
        return f"Prescription for {self.patient} by Dr. {self.doctor.get_full_name()}"

    def update_status(self, new_status):
        """Update the status of the prescription and log the change."""
        if new_status in dict(self._meta.get_field('status').choices):
            self.history += f"{self.status} -> {new_status} on {self.issue_date}\n"
            self.status = new_status
            self.save()


class Dispensation(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity_dispensed = models.PositiveIntegerField()
    date_dispensed = models.DateTimeField(auto_now_add=True)
    dispensed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Pharmacist
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()

    def __str__(self):
        return f"Dispensation of {self.medication.name} from Prescription {self.prescription.id}"

    def save(self, *args, **kwargs):
        """Ensure medication batch and expiry details are updated."""
        medication = self.medication
        if medication.batch_number != self.batch_number or medication.expiry_date != self.expiry_date:
            raise ValueError("Batch number or expiry date mismatch.")
        if medication.is_expired():
            raise ValueError("Cannot dispense expired medication.")
        medication.adjust_stock(-self.quantity_dispensed)
        super().save(*args, **kwargs)
