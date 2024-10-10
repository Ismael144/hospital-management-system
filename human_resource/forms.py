from accounts.models import Employee
from .models import *
from django import forms 
from django.db.models import Q

class TrainingParticipantForm(forms.ModelForm):
    class Meta:
        model = TrainingParticipant
        fields = ['employee', 'training', 'completion_date', 'certificate_issued']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter employees to exclude HR Managers
        self.fields['employee'].queryset = Employee.objects.filter(~Q(role='hr_manager'))
        

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['employee', 'shift', 'department', 'notes']
        
    department = forms.Select()
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes'})
    )

class NoticeBoardForm(forms.ModelForm):
    class Meta:
        model = NoticeBoard
        fields = ['title', 'content', 'category', 'tags', 'expires_on']

    expires_on = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 5})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control'})
        self.fields['expires_on'].widget.attrs.update({'class': 'form-control', 'type': 'datetime-local'})

    def clean(self):
        cleaned_data = super().clean()
        expires_on = cleaned_data.get('expires_on')
        if expires_on and expires_on < timezone.now():
            self.add_error('expires_on', 'Expiration date cannot be in the past.')


class StaffOnDutyForm(forms.ModelForm):
    class Meta:
        model = StaffOnDuty
        fields = ['employee', 'date', 'shift_start', 'shift_end', 'department']
        
    # Customize field widgets if necessary
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    shift_start = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    shift_end = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    department = forms.Select()


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = [
            'name', 
            'description', 
            'shift_start_time', 
            'shift_stop_time', 
            'shift_type', 
            'days_of_week', 
            'break_start_time', 
            'break_stop_time', 
            'is_active'
        ]
        widgets = {
            'shift_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'shift_stop_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_stop_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'days_of_week': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head', 'is_active']
        
        
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason', 'status']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_by': forms.Select(attrs={'class': 'form-control'}),
        }