# views.py

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Medication, Prescription, Dispensation
from .forms import MedicationForm, PrescriptionForm, DispensationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from activities.models import Activity
from django.utils import timezone
from .models import MedicationAssignment
from .forms import MedicationAssignmentForm
from django.contrib import messages

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


class MedicationAssignmentListView(LoginRequiredMixin, ListView):
    model = MedicationAssignment
    template_name = 'medication_assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        # Log the activity
        Activity.objects.create(
            user=self.request.user,
            action='viewed',
            description='Viewed the medication assignment list.',
            timestamp=timezone.now()
        )
        print(super().get_queryset())
        return super().get_queryset()


class MedicationAssignmentDetailView(LoginRequiredMixin, DetailView):
    model = MedicationAssignment
    template_name = 'medication_assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Log the activity
        Activity.objects.create(
            user=self.request.user,
            action='viewed',
            description=f'Viewed medication assignment details for {self.object.patient.user.get_full_name()}.',
            timestamp=timezone.now()
        )
        return context


class MedicationAssignmentCreateView(LoginRequiredMixin, CreateView):
    model = MedicationAssignment
    form_class = MedicationAssignmentForm
    template_name = 'medication_assignment_form.html'
    success_url = reverse_lazy('medication-assignment-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the activity
        Activity.objects.create(
            user=self.request.user,
            action='created',
            description=f'Created a new medication assignment for {self.object.patient.user.get_full_name()}.',
            timestamp=timezone.now()
        )
        
        print("Errors: ", self.form_class.errors)
        
        # Set session message
        messages.success(self.request, f'A new medication assignment has been created for you by Dr. {self.object.prescribing_doctor.employee.user.get_full_name()}.')
        
        return response


class MedicationAssignmentUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicationAssignment
    form_class = MedicationAssignmentForm
    template_name = 'medication_assignment_form.html'
    success_url = reverse_lazy('medication-assignment-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the activity
        Activity.objects.create(
            user=self.request.user,
            action='updated',
            description=f'Updated the medication assignment for {self.object.patient.user.get_full_name()}.',
            timestamp=timezone.now()
        )
        # Send a message
        messages.success(self.request, f'Your medication assignment has been updated by Dr. {self.object.prescribing_doctor.employee.user.get_full_name()}.')
        
        return response


class MedicationAssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicationAssignment
    template_name = 'medication_assignment_confirm_delete.html'
    success_url = reverse_lazy('medication-assignment-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Log the activity
        Activity.objects.create(
            user=request.user,
            action='deleted',
            description=f'Deleted the medication assignment for {self.object.patient.user.get_full_name()}.',
            timestamp=timezone.now()
        )
        # Send a message
        messages.success(self.request, f'Your medication assignment has been updated by Dr. {self.object.prescribing_doctor.employee.user.get_full_name()}.')

        return super().delete(request, *args, **kwargs)