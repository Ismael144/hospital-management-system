from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from laboratory.models import LabTest
from django.core.files.storage import default_storage

def user_directory_path(instance, filename):
    # Randomize ID
    import random 
    rand_int = random.randint(14000, 54000)
    return f'user_{instance.pk}_{filename}_{rand_int}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('patient', 'Patient'),
        ('receptionist', 'Receptionist'), 
        ('pharmacist', 'Pharmacist'), 
        ('case_manager', 'Case Manager'), 
        ('laboratorist', 'Laboratorist'),
        ('accountant', 'Accountant'),
        ('hr_manager', 'Human Resource Manager')
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self) -> str: 
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f'{self.get_full_name()}({self.role})'

    def save(self, *args, **kwargs):
        # Check if the profile_image has changed
        if self.pk:
            old_user = CustomUser.objects.get(pk=self.pk)
            if old_user.profile_image and old_user.profile_image != self.profile_image:
                # Delete the old profile image
                if default_storage.exists(old_user.profile_image.path):
                    default_storage.delete(old_user.profile_image.path)
        
        super().save(*args, **kwargs)


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('rather_not_say', 'Rather Not Say')])
    hire_date = models.DateField()
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    certificate = models.FileField(upload_to='staff/certificates/', null=True, blank=True)
    
    def __str__(self):
        return f'{str(self.user.get_full_name()).capitalize()}({self.user.role.capitalize()})'


class Receptionist(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='receptionist_profile', null=True)
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.employee.user.email


class Doctor(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='doctor_profile', null=True)
    specialization = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    medical_license_number = models.CharField(max_length=50)
    board_certifications = models.TextField()
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    current_patient_load = models.IntegerField(default=0)
    appointment_schedule = models.TextField(blank=True, null=True)
    recent_treatments = models.TextField(blank=True, null=True)
    recent_training = models.TextField(blank=True, null=True)
    performance_reviews = models.TextField(blank=True, null=True)
    department = models.ForeignKey('human_resource.Department', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.employee.user.get_full_name()


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    medical_history = models.TextField()
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=50, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    family_medical_history = models.TextField(blank=True, null=True)
    health_habits = models.TextField(blank=True, null=True)
    disease = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=70, choices=[('In Treatment', 'In Treatment'), ('New Patient', 'New Patient'), ('Recovered', 'Recovered'), ('discharged', 'Discharged')])
    assigned_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_room = models.ForeignKey('facilities.Room', null=True, blank=True, on_delete=models.SET_NULL, related_name='patients')
    document = models.FileField(upload_to='patients/documents', null=True, blank=True)
    preferred_language = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class DischargeSummary(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='discharge_summaries')
    discharge_date = models.DateField(blank=True, null=True)
    discharge_instructions = models.TextField(blank=True, null=True)
    follow_up_appointments = models.TextField(blank=True, null=True)
    discharge_status = models.CharField(
        max_length=50,
        choices=[
            ('Planned', 'Planned'),
            ('Completed', 'Completed'),
            ('Pending', 'Pending'),
        ],
        default='Pending',
    )
    discharge_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    treatment_summary = models.TextField(blank=True, null=True)
    medication_at_discharge = models.TextField(blank=True, null=True)
    condition_at_discharge = models.TextField(blank=True, null=True)
    discharge_reason = models.CharField(max_length=255, blank=True, null=True)
    support_services_required = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Discharge Summary for {self.patient.user.get_full_name()}"


class MedicalReport(models.Model):
    patient = models.ForeignKey('accounts.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_examination = models.DateTimeField()
    chief_complaint = models.TextField()
    history_of_present_illness = models.TextField()
    past_medical_history = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    physical_examination = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    follow_up_instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Report for {self.patient} on {self.date_of_examination}"


class Nurse(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='nurse_profile', null=True)
    qualifications = models.TextField()
    years_of_experience = models.IntegerField()
    license_number = models.CharField(max_length=50)
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    current_patient_load = models.IntegerField(default=0)
    recent_trainings = models.TextField(blank=True, null=True)
    performance_reviews = models.TextField(blank=True, null=True)
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.employee.user.get_full_name()


class Pharmacist(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='pharmacist_profile', null=True)
    registration_number = models.CharField(max_length=100, unique=True)
    qualifications = models.TextField(blank=True, null=True)
    years_of_experience = models.TextField(blank=True, null=True)
    pharmacy_license_number = models.CharField(max_length=100)
    current_medication_load  = models.CharField(max_length=100)
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    license_expiry_date = models.DateField()
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"Pharmacist Profile for {self.employee.user.get_full_name()}"

    def is_license_expired(self):
        """Check if the pharmacist's license is expired."""
        from datetime import date
        return self.license_expiry_date < date.today()


class CaseManager(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='case_manager_profile', null=True)
    qualifications = models.TextField(blank=True, null=True)
    assigned_cases = models.ManyToManyField('case_management.Case', blank=True, related_name='case_managers')
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    case_load = models.IntegerField(default=0)
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.employee.user.get_full_name()}"
    

class LabTechnician(models.Model):
    LAB_SPECIALIZATION_CHOICES = [
        ('microbiology', 'Microbiology'),
        ('chemistry', 'Chemistry'),
        ('pathology', 'Pathology'),
        ('hematology', 'Hematology'),
        ('immunology', 'Immunology'),
        ('tansfusion_medicine', 'Transfusion medicine'),
        ('toxicology', 'Toxicology'),
        ('molecular_diagnostics', 'Molecular Diagnostics'),
    ]
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='laboratorist_profile', null=True)
    qualifications = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    assigned_tests = models.ManyToManyField(LabTest, blank=True, related_name='assigned_laboratorists')
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    current_lab_load = models.IntegerField(default=0)
    lab_specialization = models.CharField(choices=LAB_SPECIALIZATION_CHOICES, max_length=40)
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"Profile for {self.employee.user.get_full_name()}"
    
    
class Accountant(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='accountant_profile', null=True)
    qualifications = models.TextField(blank=True, null=True)
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    years_of_experience = models.IntegerField()
    recent_training = models.TextField(blank=True, null=True)
    performance_reviews = models.TextField(blank=True, null=True)
    current_account_load = models.IntegerField(default=0)
    recent_trainings = models.TextField(null=True, blank=True)
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.employee.user.get_full_name()


class Representative(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    date_hired = models.DateField()
    responsibilities = models.TextField()
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - Representative'

    class Meta:
        verbose_name = 'Representative'
        verbose_name_plural = 'Representatives'
        

class HRManager(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='hr_manager_profile', null=True)
    qualifications = models.TextField(blank=True, null=True)
    shift = models.ForeignKey('human_resource.Shift', null=True, blank=True, on_delete=models.DO_NOTHING)
    years_of_experience = models.IntegerField()
    recent_training = models.TextField(blank=True, null=True)
    performance_reviews = models.TextField(blank=True, null=True)
    team_size_managed = models.IntegerField(default=0)
    current_projects = models.TextField(null=True, blank=True)
    department = models.ForeignKey('human_resource.Department', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.employee.user.get_full_name()