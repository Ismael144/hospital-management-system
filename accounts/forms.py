from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (CustomUser, Employee, Doctor, Patient, Nurse, Receptionist, 
                     Pharmacist, CaseManager, LabTechnician, Accountant, Representative, DischargeSummary)
from django.core.exceptions import ValidationError

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'password', 'email', 'role', 'is_active', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('password', None)
            
class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'password', 'address', 'phone_number', 
                  'date_of_birth', 'gender', 'hire_date', 'certificate', 'profile_image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields.pop('password', None)

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = employee.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if 'password' in self.cleaned_data and self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            employee.save()
        return employee


class DoctorForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    certificate = forms.FileField(required=False, label="Doctor's Certificate")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name','email', 'password', 'address', 'phone_number', 
                  'date_of_birth', 'gender', 'hire_date',
                  'specialization', 'years_of_experience', 'department', 
                  'medical_license_number', 'board_certifications', 'shift', 'current_patient_load', 'appointment_schedule', 
                  'recent_treatments', 'recent_training', 'performance_reviews', 'profile_image', 'certificate']
        widgets = {
            'shift': forms.Select(),
        }
        
    def clean_email(self): 
        if self.instance.pk: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('password', None)
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def save(self, commit=True):
        doctor = super(DoctorForm, self).save(commit=False)
        if not doctor.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='doctor'
            )
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            doctor.employee = employee
        else:
            doctor.employee.user.email = self.cleaned_data['email']
            doctor.employee.user.first_name = self.cleaned_data['first_name']
            doctor.employee.user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                doctor.employee.user.set_password(self.cleaned_data['password'])
            doctor.employee.user.save()
            
            doctor.employee.address = self.cleaned_data['address']
            doctor.employee.phone_number = self.cleaned_data['phone_number']
            doctor.employee.date_of_birth = self.cleaned_data['date_of_birth']
            doctor.employee.gender = self.cleaned_data['gender']
            doctor.employee.hire_date = self.cleaned_data['hire_date']
            doctor.employee.profile_image = self.cleaned_data['profile_image']
            doctor.employee.save()

        if commit:
            doctor.save()
        return doctor


class NurseForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")

    class Meta:
        model = Nurse
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number', 
                  'date_of_birth', 'gender', 'hire_date', 'profile_image', 'qualifications', 'years_of_experience', 'license_number', 
                  'shift', 'current_patient_load', 
                  'recent_trainings']
        widgets = {
            'shift': forms.Select(),
        }
        
    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email aaaddress is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address (Hello world) is not available, please use another')
        
        return email


    def __init__(self, *args, **kwargs):
        super(NurseForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('password', None)
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def save(self, commit=True):
        nurse = super(NurseForm, self).save(commit=False)
        if not nurse.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='nurse'
            )
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            nurse.employee = employee
        else:
            nurse.employee.user.email = self.cleaned_data['email']
            nurse.employee.user.first_name = self.cleaned_data['first_name']
            nurse.employee.user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                nurse.employee.user.set_password(self.cleaned_data['password'])
            nurse.employee.user.save()
            
            nurse.employee.address = self.cleaned_data['address']
            nurse.employee.phone_number = self.cleaned_data['phone_number']
            nurse.employee.date_of_birth = self.cleaned_data['date_of_birth']
            nurse.employee.gender = self.cleaned_data['gender']
            nurse.employee.hire_date = self.cleaned_data['hire_date']
            nurse.employee.profile_image = self.cleaned_data['profile_image']
            nurse.employee.save()

        if commit:
            nurse.save()
        return nurse


class ReceptionistForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    certificate = forms.FileField(required=False, label="Receptionist's Certificate")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")

    class Meta:
        model = Receptionist
        fields = ['first_name', 'last_name', 'email', 'password', 'address', 'phone_number', 'date_of_birth', 
                  'gender', 'hire_date', 'shift', 'profile_image', 
                   'certificate']
        widgets = {
            'shift': forms.Select(),
        }
         
    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def __init__(self, *args, **kwargs):
        super(ReceptionistForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('password', None)
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def save(self, commit=True):
        receptionist = super(ReceptionistForm, self).save(commit=False)
        if not receptionist.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='receptionist'
            )
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            receptionist.employee = employee
        else:
            receptionist.employee.user.email = self.cleaned_data['email']
            receptionist.employee.user.first_name = self.cleaned_data['first_name']
            receptionist.employee.user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                receptionist.employee.user.set_password(self.cleaned_data['password'])
            receptionist.employee.user.save()
            
            receptionist.employee.address = self.cleaned_data['address']
            receptionist.employee.phone_number = self.cleaned_data['phone_number']
            receptionist.employee.date_of_birth = self.cleaned_data['date_of_birth']
            receptionist.employee.gender = self.cleaned_data['gender']
            receptionist.employee.hire_date = self.cleaned_data['hire_date']
            receptionist.employee.profile_image = self.cleaned_data['profile_image']
            receptionist.employee.save()

        if commit:
            receptionist.save()
        return receptionist


class PatientForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'email', 'address', 'phone_number', 
            'date_of_birth', 'medical_history', 'emergency_contact_name',
            'emergency_contact_phone', 'insurance_provider', 'insurance_policy_number',
            'allergies', 'current_medications', 'family_medical_history',
            'health_habits', 'disease', 'status', 'assigned_doctor', 'assigned_room',
            'preferred_language'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email


    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        patient = super(PatientForm, self).save(commit=False)
        if not patient.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='patient'
            )
            patient.user = user
        else:
            patient.user.email = self.cleaned_data['email']
            patient.user.first_name = self.cleaned_data['first_name']
            patient.user.last_name = self.cleaned_data['last_name']
            patient.user.save()

        if commit:
            patient.save()
        return patient


class PharmacistForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    address = forms.CharField(max_length=255, label="Address")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    certificate = forms.FileField(required=False, label="Pharmacist's Certificate")
    years_of_experience = forms.CharField(max_length=20, label="Years Of Experience")
    license_expiry_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="License Expiry Date"
    )
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")
    
    class Meta:
        model = Pharmacist
        fields = [
            'first_name', 'last_name', 'email', 'password', 'phone_number', 'address', 
            'date_of_birth', 'gender', 'hire_date', 'pharmacy_license_number', 
            'years_of_experience', 'certificate', 'license_expiry_date', 'profile_image',
        ]

    def __init__(self, *args, **kwargs):
        super(PharmacistForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-fill fields based on the associated employee data
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def save(self, commit=True):
        pharmacist = super(PharmacistForm, self).save(commit=False)
        if not pharmacist.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='pharmacist'
            )
            user.set_password(CustomUser.objects.make_random_password())  # Set a random password
            user.save()

            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            pharmacist.employee = employee
        else:
            pharmacist.employee.user.email = self.cleaned_data['email']
            pharmacist.employee.user.first_name = self.cleaned_data['first_name']
            pharmacist.employee.user.last_name = self.cleaned_data['last_name']
            pharmacist.employee.address = self.cleaned_data['address']
            pharmacist.employee.phone_number = self.cleaned_data['phone_number']
            pharmacist.employee.date_of_birth = self.cleaned_data['date_of_birth']
            pharmacist.employee.gender = self.cleaned_data['gender']
            pharmacist.employee.hire_date = self.cleaned_data['hire_date']
            pharmacist.employee.profile_image = self.cleaned_data['profile_image']
            pharmacist.employee.save()
            pharmacist.employee.user.save()

        # Set the license_expiry_date for the pharmacist
        pharmacist.license_expiry_date = self.cleaned_data['license_expiry_date']

        if commit:
            pharmacist.save()
        return pharmacist 

            
class CaseManagerForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    certificate = forms.FileField(required=False, label="Case Manager's Certificate")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")

    class Meta:
        model = CaseManager
        fields = [
            'first_name', 'last_name', 'email', 'address', 'password', 'phone_number', 
            'date_of_birth', 'gender', 'certificate', 'hire_date', 'profile_image',
            'case_load'
        ]

    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def __init__(self, *args, **kwargs):
        super(CaseManagerForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def save(self, commit=True):
        case_manager = super(CaseManagerForm, self).save(commit=False)
        if not case_manager.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='case_manager'
            )
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            case_manager.employee = employee
        else:
            case_manager.employee.user.email = self.cleaned_data['email']
            case_manager.employee.user.first_name = self.cleaned_data['first_name']
            case_manager.employee.user.last_name = self.cleaned_data['last_name']
            case_manager.employee.user.save()
            
            case_manager.employee.address = self.cleaned_data['address']
            case_manager.employee.phone_number = self.cleaned_data['phone_number']
            case_manager.employee.date_of_birth = self.cleaned_data['date_of_birth']
            case_manager.employee.gender = self.cleaned_data['gender']
            case_manager.employee.hire_date = self.cleaned_data['hire_date']
            case_manager.employee.profile_image = self.cleaned_data['profile_image']
            case_manager.employee.save()

        if commit:
            case_manager.save()
        return case_manager


class AccountantForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    certificate = forms.FileField(required=False, label="Accountant's Certificate")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")

    class Meta:
        model = Accountant
        fields = [
            'first_name', 'last_name', 'email', 'address', 'password', 'phone_number', 
            'date_of_birth', 'gender', 'hire_date', 'years_of_experience', 'certificate', 'profile_image',
        ]

    def __init__(self, *args, **kwargs):
        super(AccountantForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def save(self, commit=True):
        accountant = super(AccountantForm, self).save(commit=False)
        if not accountant.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='accountant'
            )
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            accountant.employee = employee
        else:
            accountant.employee.user.email = self.cleaned_data['email']
            accountant.employee.user.first_name = self.cleaned_data['first_name']
            accountant.employee.user.last_name = self.cleaned_data['last_name']
            accountant.employee.user.save()
            
            accountant.employee.address = self.cleaned_data['address']
            accountant.employee.phone_number = self.cleaned_data['phone_number']
            accountant.employee.date_of_birth = self.cleaned_data['date_of_birth']
            accountant.employee.gender = self.cleaned_data['gender']
            accountant.employee.hire_date = self.cleaned_data['hire_date']
            accountant.employee.profile_image = self.cleaned_data['profile_image']
            accountant.employee.save()

        if commit:
            accountant.save()
        return accountant


class RepresentativeForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    certificate = forms.FileField(required=False, label="Representative's Certificate")

    class Meta:
        model = Representative
        fields = [
            'email', 'first_name', 'last_name', 'address', 'phone_number', 
            'date_of_birth', 'gender', 'certificate', 'hire_date', 'profile_image'
        ]

    def __init__(self, *args, **kwargs):
        super(RepresentativeForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def save(self, commit=True):
        representative = super(RepresentativeForm, self).save(commit=False)
        if not representative.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='representative'
            )
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            representative.employee = employee
        else:
            representative.employee.user.email = self.cleaned_data['email']
            representative.employee.user.first_name = self.cleaned_data['first_name']
            representative.employee.user.last_name = self.cleaned_data['last_name']
            representative.employee.user.save()
            
            representative.employee.address = self.cleaned_data['address']
            representative.employee.phone_number = self.cleaned_data['phone_number']
            representative.employee.date_of_birth = self.cleaned_data['date_of_birth']
            representative.employee.gender = self.cleaned_data['gender']
            representative.employee.hire_date = self.cleaned_data['hire_date']
            representative.employee.profile_image = self.cleaned_data['profile_image']
            representative.employee.save()

        if commit:
            representative.save()
        return representative


class DischargeSummaryForm(forms.ModelForm):
    class Meta:
        model = DischargeSummary
        fields = [
            'patient',
            'discharge_date',
            'discharge_instructions',
            'follow_up_appointments',
            'discharge_status',
            'discharge_doctor',
            'treatment_summary',
            'medication_at_discharge',
            'condition_at_discharge',
            'discharge_reason',
            'support_services_required',
        ]
        widgets = {
            'discharge_date': forms.DateInput(attrs={'type': 'date'}),
            'discharge_instructions': forms.Textarea(attrs={'rows': 3}),
            'follow_up_appointments': forms.Textarea(attrs={'rows': 3}),
            'treatment_summary': forms.Textarea(attrs={'rows': 3}),
            'medication_at_discharge': forms.Textarea(attrs={'rows': 3}),
            'condition_at_discharge': forms.Textarea(attrs={'rows': 3}),
            'support_services_required': forms.Textarea(attrs={'rows': 3}),
        }
        

class LabTechnicianForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=255, label="Address")
    phone_number = forms.CharField(max_length=20, label="Phone Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label="Gender")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Hire Date")
    profile_image = forms.ImageField(required=False, label="Profile Image")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password")

    class Meta:
        model = LabTechnician
        fields = ['first_name', 'last_name', 'email', 'password', 'address', 'phone_number', 
                  'date_of_birth', 'gender', 'hire_date', 'qualifications', 
                  'lab_specialization', 'years_of_experience', 'shift', 'current_lab_load', 
                  'department', 'assigned_tests', 'profile_image']
        widgets = {
            'shift': forms.Select(),
            'department': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(LabTechnicianForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields.pop('password', None)
            self.fields['email'].initial = self.instance.employee.user.email
            self.fields['first_name'].initial = self.instance.employee.user.first_name
            self.fields['last_name'].initial = self.instance.employee.user.last_name
            self.fields['address'].initial = self.instance.employee.address
            self.fields['phone_number'].initial = self.instance.employee.phone_number
            self.fields['date_of_birth'].initial = self.instance.employee.date_of_birth
            self.fields['gender'].initial = self.instance.employee.gender
            self.fields['hire_date'].initial = self.instance.employee.hire_date
            self.fields['profile_image'].initial = self.instance.employee.profile_image

    def clean_email(self): 
        if self.instance: 
            email = self.cleaned_data.get('email')
            if CustomUser.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists(): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        else:
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email): 
                raise ValidationError('Sorry, this email address is not available, please use another')
        
        return email

    def save(self, commit=True):
        lab_technician = super(LabTechnicianForm, self).save(commit=False)
        if not lab_technician.pk:
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='lab_technician'
            )
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            employee = Employee.objects.create(
                user=user,
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                hire_date=self.cleaned_data['hire_date'],
                profile_image=self.cleaned_data['profile_image']
            )
            lab_technician.employee = employee
        else:
            lab_technician.employee.user.email = self.cleaned_data['email']
            lab_technician.employee.user.first_name = self.cleaned_data['first_name']
            lab_technician.employee.user.last_name = self.cleaned_data['last_name']
            if self.cleaned_data['password']:
                lab_technician.employee.user.set_password(self.cleaned_data['password'])
            lab_technician.employee.user.save()
            
            lab_technician.employee.address = self.cleaned_data['address']
            lab_technician.employee.phone_number = self.cleaned_data['phone_number']
            lab_technician.employee.date_of_birth = self.cleaned_data['date_of_birth']
            lab_technician.employee.gender = self.cleaned_data['gender']
            lab_technician.employee.hire_date = self.cleaned_data['hire_date']
            lab_technician.employee.profile_image = self.cleaned_data['profile_image']
            lab_technician.employee.save()

        if commit:
            lab_technician.save()
            # Update the many-to-many field `assigned_tests`
            self.save_m2m()
        return lab_technician
