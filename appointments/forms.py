from django import forms
from .models import Appointment
from accounts.models import Patient, Employee

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        

        if self.user and self.user.is_authenticated:
            role = getattr(self.user, 'role', '').lower()
            
            if role == 'patient':
                self.fields['patient'].widget = forms.HiddenInput()
                self.fields['patient'].label = ''
                try:
                    self.fields['patient'].initial = Patient.objects.get(user=self.user)
                except Patient.DoesNotExist:
                    pass
            elif role in ['lab_technician', 'case_manager', 'nurse', 'employee', 'pharmacist']:
                # Hide employee fields
                self.fields['employee'].widget = forms.HiddenInput()
                self.fields['employee'].label = ''
                
                try:
                    employee = Employee.objects.get(user=self.user)
                    if employee is not None:
                        print(employee)
                        if role == employee.user.role:
                            self.fields['employee'].initial = Employee.objects.get(user=self.user)
                except (Employee.DoesNotExist, Employee.DoesNotExist):
                    pass
            
            employee = Employee.objects.filter(user=self.user).first()
            # Make the non-applicable field required=False
            if employee is not None: 
                if role == employee.user.role:
                    self.fields['employee'].required = False
                
    class Meta:
        model = Appointment
        fields = ['patient', 'employee', 'appointment_date', 'reason']
        widgets = {
            'patient': forms.Select(attrs={'class':'form-control select2'}),
            'employee': forms.Select(attrs={'class':'form-control select2'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        employee = cleaned_data.get("employee")

        if employee and Appointment.objects.filter(employee=employee, appointment_date=appointment_date).exists():
            self.add_error('employee', 'The selected employee is not available at this time.')

        return cleaned_data

    
class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'employee', 'appointment_date', 'reason']
        widgets = {
            'patient': forms.Select(attrs={'class':'form-control select2'}),
            'employee': forms.Select(attrs={'class':'form-control select2'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        employee = cleaned_data.get("employee")

        if employee and Appointment.objects.filter(employee=employee, appointment_date=appointment_date).exists():
            self.add_error('employee', 'The selected employee is not available at this time.')

        return cleaned_data