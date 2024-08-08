from django import forms
from .models import Attendance
from django import forms
from .models import Attendance
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AttendanceSearchForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=True, label="User")
    date = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label="Date")


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'date', 'time_in', 'time_out']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'time_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
