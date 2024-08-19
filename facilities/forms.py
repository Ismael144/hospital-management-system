from django import forms 
from .models import Allocation, Room
from .models import Inventory
from .models import Supplier

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
        

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'status', 'room_type', 'capacity']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'room_number': 'Room Number',
            'status': 'Room Status',
            'room_type': 'Room Type',
            'capacity': 'Capacity',
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity < 0:
            raise forms.ValidationError("Capacity cannot be negative.")
        return capacity


class InventoryForm(forms.ModelForm):
    item_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    unit_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quantity_in_stock = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    reorder_threshold = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Inventory
        fields = ['item_name', 'description', 'quantity', 'unit_price', 'quantity_in_stock', 'reorder_threshold', 'supplier', 'expiry_date']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'description', 'location']