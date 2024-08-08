from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract 'user' from kwargs
        super().__init__(*args, **kwargs)
        self.user = user  # Store 'user' as an instance attribute

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'nurse', 'appointment_date', 'reason']
        widgets = {
            'patient': forms.Select(attrs={'class':'form-control select2'}),
            'doctor': forms.Select(attrs={'class':'form-control select2'}),
            'nurse': forms.Select(attrs={'class':'form-control select2'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'datetime-local'}),
            'appointment_time': forms.TimeInput(attrs={'class': 'form-control datetimepicker-input', 'type': 'time'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get("appointment_date")
        doctor = cleaned_data.get("doctor")
        nurse = cleaned_data.get("nurse")

        # Check for doctor availability
        if doctor and Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date).exists():
            self.add_error('doctor', 'The selected doctor is not available at this time.')

        # Check for nurse availability
        if nurse and Appointment.objects.filter(nurse=nurse, appointment_date=appointment_date).exists():
            self.add_error('nurse', 'The selected nurse is not available at this time.')
            
        if doctor is not None and nurse is not None: 
            self.add_error('doctor', 'You can only have an appointment with either a doctor or a nurse but not both.')

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
