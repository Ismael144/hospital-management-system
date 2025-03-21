from django import forms
from .models import LabTest, Specimen, LabEquipment, LabResult, LaboratoryInventory

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['patient', 'test_name', 'test_code', 'status', 'results']
        widgets = {
            'status': forms.Select(choices=LabTest.STATUS_CHOICES),
        }

class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['lab_test', 'specimen_type', 'collection_date', 'condition', 'notes']
        widgets = {
            'condition': forms.Select(choices=Specimen.CONDITION_CHOICES),
            'collection_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class LabEquipmentForm(forms.ModelForm):
    class Meta:
        model = LabEquipment
        fields = ['name', 'serial_number', 'date_purchased', 'last_maintenance_date', 'next_maintenance_due', 'calibration_status']
        widgets = {
            'calibration_status': forms.Select(choices=LabEquipment.CALIBRATION_STATUS_CHOICES),
            'date_purchased': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'fp'}),
            'last_maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_maintenance_due': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        exclude = ['date_performed']  # Correctly exclude the non-editable field

class LaboratoryInventoryForm(forms.ModelForm):
    class Meta:
        model = LaboratoryInventory
        fields = ['name', 'quantity', 'description']
