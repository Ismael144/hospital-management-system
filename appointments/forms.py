from django import forms
from .models import Appointment
from accounts.models import Patient, Doctor, Employee

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
            elif role in ['doctor', 'nurse']:
                # Hide both doctor and nurse fields
                self.fields['doctor'].widget = forms.HiddenInput()
                self.fields['doctor'].label = ''
                self.fields['nurse'].widget = forms.HiddenInput()
                self.fields['nurse'].label = ''
                
                try:
                    employee = Employee.objects.get(user=self.user)
                    if role == 'doctor':
                        self.fields['doctor'].initial = Doctor.objects.get(employee=employee)
                    else:  # nurse
                        self.fields['nurse'].initial = employee
                except (Employee.DoesNotExist, Doctor.DoesNotExist):
                    pass

            # Make the non-applicable field required=False
            if role == 'doctor':
                self.fields['nurse'].required = False
            elif role == 'nurse':
                self.fields['doctor'].required = False
                

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'nurse', 'appointment_date', 'reason']
        widgets = {
            'patient': forms.Select(attrs={'class':'form-control select2'}),
            'doctor': forms.Select(attrs={'class':'form-control select2'}),
            'nurse': forms.Select(attrs={'class':'form-control select2'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        doctor = cleaned_data.get("doctor")
        nurse = cleaned_data.get("nurse")

        if doctor and Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date).exists():
            self.add_error('doctor', 'The selected doctor is not available at this time.')

        if nurse and Appointment.objects.filter(nurse=nurse, appointment_date=appointment_date).exists():
            self.add_error('nurse', 'The selected nurse is not available at this time.')
            
        if doctor and nurse: 
            self.add_error('doctor', 'You can only have an appointment with either a doctor or a nurse but not both.')
            self.add_error('nurse', 'You can only have an appointment with either a doctor or a nurse but not both.')

        return cleaned_data

    
class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'nurse', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        doctor = cleaned_data.get("doctor")
        nurse = cleaned_data.get("nurse")

        if doctor is not None and nurse is not None: 
            self.add_error('doctor', 'You can only have an appointment with either a doctor or a nurse but not both.')

        # Check for doctor availability
        if doctor and Appointment.objects.exclude(doctor=doctor, appointment_date=self.instance.appointment_date).filter(doctor=doctor, appointment_date=appointment_date).exists():
            self.add_error('doctor', 'The selected doctor is not available at this time.')

        # Check for nurse availability
        if nurse and Appointment.objects.exclude(nurse=nurse, appointment_date=self.instance.appointment_date).filter(nurse=nurse, appointment_date=appointment_date).exists():
            self.add_error('nurse', 'The selected nurse is not available at this time.')


        return cleaned_data
