from django import forms 
from .models import Allocation, Room
from .models import Inventory

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['patient', 'allocation_type', 'room', 'sickbay']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'allocation_type': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'sickbay': forms.Select(attrs={'class': 'form-control'}),
        }

class InventoryCreateForm(forms.ModelForm):
    item_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    unit_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Inventory
        fields = ['item_name', 'description', 'quantity', 'unit_price']


class InventoryUpdateForm(forms.ModelForm):
    item_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    unit_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Inventory
        fields = ['item_name', 'description', 'quantity', 'unit_price']