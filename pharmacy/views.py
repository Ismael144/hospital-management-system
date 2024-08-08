from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Medication, Prescription, Dispensation
from .forms import MedicationForm, PrescriptionForm, DispensationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import PharmacyInventory
from .forms import PharmacyInventoryForm

class MedicationListView(ListView):
    model = Medication
    template_name = 'pharmacy/medication_list.html'
    context_object_name = 'medications'


class MedicationDetailView(DetailView):
    model = Medication
    template_name = 'pharmacy/medication_detail.html'
    context_object_name = 'medication'


class MedicationCreateView(SuccessMessageMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'pharmacy/medication_form.html'
    success_url = reverse_lazy('medication_list')
    success_message = "Medication created successfully"


class MedicationUpdateView(SuccessMessageMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'pharmacy/medication_form.html'
    success_url = reverse_lazy('medication_list')
    success_message = "Medication updated successfully"


class MedicationDeleteView(SuccessMessageMixin, DeleteView):
    model = Medication
    template_name = 'pharmacy/medication_confirm_delete.html'
    success_url = reverse_lazy('medication_list')
    success_message = "Medication deleted successfully"


class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'pharmacy/prescription_list.html'
    context_object_name = 'prescriptions'


class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = 'pharmacy/prescription_detail.html'
    context_object_name = 'prescription'


class PrescriptionCreateView(SuccessMessageMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'pharmacy/prescription_form.html'
    success_url = reverse_lazy('prescription_list')
    success_message = "Prescription created successfully"


class PrescriptionUpdateView(SuccessMessageMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'pharmacy/prescription_form.html'
    success_url = reverse_lazy('prescription_list')
    success_message = "Prescription updated successfully"


class PrescriptionDeleteView(SuccessMessageMixin, DeleteView):
    model = Prescription
    template_name = 'pharmacy/prescription_confirm_delete.html'
    success_url = reverse_lazy('prescription_list')
    success_message = "Prescription deleted successfully"


class DispensationListView(ListView):
    model = Dispensation
    template_name = 'pharmacy/dispensation_list.html'
    context_object_name = 'dispensations'


class DispensationDetailView(DetailView):
    model = Dispensation
    template_name = 'pharmacy/dispensation_detail.html'
    context_object_name = 'dispensation'


class DispensationCreateView(SuccessMessageMixin, CreateView):
    model = Dispensation
    form_class = DispensationForm
    template_name = 'pharmacy/dispensation_form.html'
    success_url = reverse_lazy('dispensation_list')
    success_message = "Medication dispensed successfully"


class DispensationUpdateView(SuccessMessageMixin, UpdateView):
    model = Dispensation
    form_class = DispensationForm
    template_name = 'pharmacy/dispensation_form.html'
    success_url = reverse_lazy('dispensation_list')
    success_message = "Dispensation updated successfully"


class DispensationDeleteView(SuccessMessageMixin, DeleteView):
    model = Dispensation
    template_name = 'pharmacy/dispensation_confirm_delete.html'
    success_url = reverse_lazy('dispensation_list')
    success_message = "Dispensation deleted successfully"
    

class InventoryListView(View):
    def get(self, request):
        inventories = PharmacyInventory.objects.all()
        return render(request, 'pharmacy/inventory_list.html', {'inventories': inventories})

class InventoryDetailView(View):
    def get(self, request, pk):
        inventory = get_object_or_404(PharmacyInventory, pk=pk)
        return render(request, 'pharmacy/inventory_detail.html', {'inventory': inventory})

class InventoryCreateView(View):
    def get(self, request):
        form = PharmacyInventoryForm()
        return render(request, 'pharmacy/inventory_form.html', {'form': form, 'title': 'Add Inventory'})

    def post(self, request):
        form = PharmacyInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('inventory_list'))
        return render(request, 'pharmacy/inventory_form.html', {'form': form, 'title': 'Add Inventory'})

class InventoryUpdateView(View):
    def get(self, request, pk):
        inventory = get_object_or_404(PharmacyInventory, pk=pk)
        form = PharmacyInventoryForm(instance=inventory)
        return render(request, 'pharmacy/inventory_form.html', {'form': form, 'title': 'Update Inventory'})

    def post(self, request, pk):
        inventory = get_object_or_404(PharmacyInventory, pk=pk)
        form = PharmacyInventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect(reverse('inventory_list'))
        return render(request, 'pharmacy/inventory_form.html', {'form': form, 'title': 'Update Inventory'})

class InventoryDeleteView(View):
    def get(self, request, pk):
        inventory = get_object_or_404(PharmacyInventory, pk=pk)
        return render(request, 'pharmacy/inventory_confirm_delete.html', {'inventory': inventory})

    def post(self, request, pk):
        inventory = get_object_or_404(PharmacyInventory, pk=pk)
        inventory.delete()
        return redirect(reverse('inventory_list'))
