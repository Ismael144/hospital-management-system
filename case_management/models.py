from django.db import models
from django.conf import settings

class Case(models.Model):
    STATUS_CHOICES = [('Open', 'Open'), 
                      ('Closed', 'Closed'), 
                      ('Pending', 'Pending')]

    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    case_manager = models.ForeignKey("accounts.CaseManager", on_delete=models.CASCADE)
    case_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Case {self.case_number} - {self.patient}"

    def close_case(self):
        """Mark the case as closed."""
        self.status = 'Closed'
        self.save()
        

class CaseNote(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Case manager
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.case}"


class CarePlan(models.Model):
    STATUS_CHOICES = [('Active', 'Active'),
                      ('Completed', 'Completed'), 
                      ('Pending', 'Pending')]
    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    plan_details = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Care Plan for {self.case.patient}"
