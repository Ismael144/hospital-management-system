# views.py

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Medication, Prescription, Dispensation
from .forms import MedicationForm, PrescriptionForm, DispensationForm, PharmacyInventoryForm
from django.views import View
from activities.models import Activity

# Utility function to log activity
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

# Medication Views

@method_decorator([login_required, permission_required('pharmacy.view_medication', raise_exception=True)], name='dispatch')
class MedicationListView(ListView):
    model = Medication
    template_name = 'pharmacy/medication_list.html'
    context_object_name = 'medications'


@method_decorator([login_required, permission_required('pharmacy.view_medication', raise_exception=True)], name='dispatch')
class MedicationDetailView(DetailView):
    model = Medication
    template_name = 'pharmacy/medication_detail.html'
    context_object_name = 'medication'


@method_decorator([login_required, permission_required('pharmacy.add_medication', raise_exception=True)], name='dispatch')
class MedicationCreateView(SuccessMessageMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'pharmacy/medication_form.html'
    success_url = reverse_lazy('medication_list')
    success_message = "Medication created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create Medication', f'Medication {self.object.name} was created.')
        return response


@method_decorator([login_required, permission_required('pharmacy.change_medication', raise_exception=True)], name='dispatch')
class MedicationUpdateView(SuccessMessageMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'pharmacy/medication_form.html'
    success_url = reverse_lazy('medication_list')
    success_message = "Medication updated successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update Medication', f'Medication {self.object.name} was updated.')
        return response


@method_decorator([login_required, permission_required('pharmacy.delete_medication', raise_exception=True)], name='dispatch')
class MedicationDeleteView(SuccessMessageMixin, DeleteView):
    model = Medication
    template_name = 'pharmacy/medication_confirm_delete.html'
    success_url = reverse_lazy('medication_list')
    success_message = "Medication deleted successfully"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete Medication', f'Medication {self.object.name} was deleted.')
        return super().delete(request, *args, **kwargs)

# Prescription Views

@method_decorator([login_required, permission_required('pharmacy.view_prescription', raise_exception=True)], name='dispatch')
class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'pharmacy/prescription_list.html'
    context_object_name = 'prescriptions'


@method_decorator([login_required, permission_required('pharmacy.view_prescription', raise_exception=True)], name='dispatch')
class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = 'pharmacy/prescription_detail.html'
    context_object_name = 'prescription'


@method_decorator([login_required, permission_required('pharmacy.add_prescription', raise_exception=True)], name='dispatch')
class PrescriptionCreateView(SuccessMessageMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'pharmacy/prescription_form.html'
    success_url = reverse_lazy('prescription_list')
    success_message = "Prescription created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create Prescription', f'Prescription {self.object.id} was created.')
        return response


@method_decorator([login_required, permission_required('pharmacy.change_prescription', raise_exception=True)], name='dispatch')
class PrescriptionUpdateView(SuccessMessageMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'pharmacy/prescription_form.html'
    success_url = reverse_lazy('prescription_list')
    success_message = "Prescription updated successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update Prescription', f'Prescription {self.object.id} was updated.')
        return response


@method_decorator([login_required, permission_required('pharmacy.delete_prescription', raise_exception=True)], name='dispatch')
class PrescriptionDeleteView(SuccessMessageMixin, DeleteView):
    model = Prescription
    template_name = 'pharmacy/prescription_confirm_delete.html'
    success_url = reverse_lazy('prescription_list')
    success_message = "Prescription deleted successfully"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete Prescription', f'Prescription {self.object.id} was deleted.')
        return super().delete(request, *args, **kwargs)

# Dispensation Views

@method_decorator([login_required, permission_required('pharmacy.view_dispensation', raise_exception=True)], name='dispatch')
class DispensationListView(ListView):
    model = Dispensation
    template_name = 'pharmacy/dispensation_list.html'
    context_object_name = 'dispensations'


@method_decorator([login_required, permission_required('pharmacy.view_dispensation', raise_exception=True)], name='dispatch')
class DispensationDetailView(DetailView):
    model = Dispensation
    template_name = 'pharmacy/dispensation_detail.html'
    context_object_name = 'dispensation'


@method_decorator([login_required, permission_required('pharmacy.add_dispensation', raise_exception=True)], name='dispatch')
class DispensationCreateView(SuccessMessageMixin, CreateView):
    model = Dispensation
    form_class = DispensationForm
    template_name = 'pharmacy/dispensation_form.html'
    success_url = reverse_lazy('dispensation_list')
    success_message = "Medication dispensed successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create Dispensation', f'Dispensation {self.object.id} was created.')
        return response


@method_decorator([login_required, permission_required('pharmacy.change_dispensation', raise_exception=True)], name='dispatch')
class DispensationUpdateView(SuccessMessageMixin, UpdateView):
    model = Dispensation
    form_class = DispensationForm
    template_name = 'pharmacy/dispensation_form.html'
    success_url = reverse_lazy('dispensation_list')
    success_message = "Dispensation updated successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update Dispensation', f'Dispensation {self.object.id} was updated.')
        return response


@method_decorator([login_required, permission_required('pharmacy.delete_dispensation', raise_exception=True)], name='dispatch')
class DispensationDeleteView(SuccessMessageMixin, DeleteView):
    model = Dispensation
    template_name = 'pharmacy/dispensation_confirm_delete.html'
    success_url = reverse_lazy('dispensation_list')
    success_message = "Dispensation deleted successfully"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete Dispensation', f'Dispensation {self.object.id} was deleted.')
        return super().delete(request, *args, **kwargs)
