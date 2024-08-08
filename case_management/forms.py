from django import forms
from .models import Case, CaseNote, CarePlan

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['patient', 'case_manager', 'case_number', 'status', 'notes']
        widgets = {
            'status': forms.Select(choices=Case.STATUS_CHOICES),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class CaseNoteForm(forms.ModelForm):
    class Meta:
        model = CaseNote
        fields = ['case', 'author', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class CarePlanForm(forms.ModelForm):
    class Meta:
        model = CarePlan
        fields = ['case', 'plan_details', 'start_date', 'end_date', 'status']
        widgets = {
            'status': forms.Select(choices=CarePlan.STATUS_CHOICES),
            'plan_details': forms.Textarea(attrs={'rows': 4}),
        }
