from django import forms
from .models import Medication, Prescription, Dispensation
from .models import PharmacyInventory

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'description', 'dosage', 'manufacturer', 'price', 'stock_quantity', 'batch_number', 'expiry_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'medication', 'instructions', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'medication': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class DispensationForm(forms.ModelForm):
    class Meta:
        model = Dispensation
        fields = ['prescription', 'medication', 'quantity_dispensed', 'dispensed_by', 'batch_number', 'expiry_date']
        widgets = {
            'prescription': forms.Select(attrs={'class': 'form-control'}),
            'medication': forms.Select(attrs={'class': 'form-control'}),
            'quantity_dispensed': forms.NumberInput(attrs={'class': 'form-control'}),
            'dispensed_by': forms.Select(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PharmacyInventoryForm(forms.ModelForm):
    class Meta:
        model = PharmacyInventory
        fields = ['medication', 'quantity_in_stock', 'reorder_threshold']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medication'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity_in_stock'].widget.attrs.update({'class': 'form-control'})
        self.fields['reorder_threshold'].widget.attrs.update({'class': 'form-control'})
