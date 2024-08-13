from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib import messages
from .models import Receptionist, Patient, Doctor, Nurse, CustomUser, DischargeSummary, Pharmacist, LabTechnician, CaseManager, Accountant
from activities.models import Activity
from .forms import PatientForm, DoctorForm, NurseForm, CustomUserForm, ReceptionistForm, DischargeSummaryForm, PharmacistForm, LabTechnicianForm, CaseManagerForm, AccountantForm
from messaging.models import Notification 
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from facilities.models import Room
from django.http import HttpResponse
# from django.urls.resolvers import escape
from facilities.forms import RoomForm
from django.utils.html import escape
from django.utils.decorators import method_decorator
from .models import Employee
from .forms import EmployeeForm

class SignInRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('signin_page')

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

# Receptionist views
class ReceptionistListView(ListView):
    model = Receptionist
    template_name = 'receptionist_list.html'
    context_object_name = 'receptionists'

class ReceptionistDetailView(DetailView):
    model = Receptionist
    template_name = 'receptionist_detail.html'
    context_object_name = 'receptionist'

class ReceptionistCreateView(View):
    template_name = 'receptionist_create.html'

    def get(self, request):
        form = ReceptionistForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ReceptionistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'Create', 'Created a new receptionist')
            return redirect('receptionist_list')
        return render(request, self.template_name, {'form': form})

class ReceptionistUpdateView(View):
    template_name = 'receptionist_update.html'

    def get(self, request, pk):
        receptionist = get_object_or_404(Receptionist, pk=pk)
        form = ReceptionistForm(request.POST, instance=receptionist)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        receptionist = get_object_or_404(Receptionist, pk=pk)
        form = ReceptionistForm(request.POST, request.FILES, instance=receptionist)
        if form.is_valid():
            cleaned_email = form.cleaned_data['email']
            email_exists = CustomUser.objects.exclude(pk=receptionist.user.pk).filter(email=cleaned_email).exists()
            if email_exists:
                form.add_error("email", "Email is not available, please use another email address...")
            else:
                form.save()
                log_activity(request.user, 'Update', f'Updated receptionist with ID {receptionist.pk}')
                return redirect('receptionist_list')
        return render(request, self.template_name, {'form': form})

class ReceptionistDeleteView(DeleteView):
    model = Receptionist
    template_name = 'receptionist_confirm_delete.html'
    success_url = reverse_lazy('receptionist_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted receptionist with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Patient views
class PatientListView(ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'
        

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patient_detail.html'
    context_object_name = 'patient'

class PatientCreateView(View):
    template_name = 'patient_create.html'

    def get(self, request):
        form = PatientForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'Create', 'Created a new patient')
            return redirect('patient_list')
        return render(request, self.template_name, {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class RoomCreatePopupView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'facilities/room_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if '_popup' in self.request.POST:
            return HttpResponse(
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (
                    escape(self.object.pk),
                    escape(self.object)
                )
            )
        return response


class PatientUpdateView(View):
    template_name = 'patient_update.html'

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        form = PatientForm(instance=patient)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            cleaned_email = form.cleaned_data['email']
            email_exists = CustomUser.objects.exclude(pk=patient.user.pk).filter(email=cleaned_email).exists()
            if email_exists:
                form.add_error("email", "Email is not available, please use another email address...")
            else:
                form.save()
                log_activity(request.user, 'Update', f'Updated patient "{patient.user.get_full_name()}"')
                return redirect('patient_list')
        return render(request, self.template_name, {'form': form})

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted patient with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Doctor views
class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'


class DoctorCreateView(View):
    template_name = 'doctor_form.html'

    def get(self, request):
        form = DoctorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'Create', 'Created a new doctor')
            return redirect('doctor_list')
        return render(request, self.template_name, {'form': form})


class DoctorUpdateView(View):
    template_name = 'doctor_form.html'

    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        form = DoctorForm(instance=doctor)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            cleaned_email = form.cleaned_data['email']
            email_exists = CustomUser.objects.exclude(pk=doctor.user.pk).filter(email=cleaned_email).exists()
            if email_exists:
                form.add_error("email", "Email is not available, please use another email address...")
            else:
                form.save()
                log_activity(request.user, 'Update', f'Updated doctor with ID {doctor.pk}')
                return redirect('doctor_list')
        return render(request, self.template_name, {'form': form})

class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted doctor with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Nurse views
class NurseListView(ListView):
    model = Nurse
    template_name = 'nurse_list.html'
    context_object_name = 'nurses'

class NurseDetailView(DetailView):
    model = Nurse
    template_name = 'nurse_detail.html'
    context_object_name = 'nurse'

class NurseCreateView(View):
    template_name = 'nurse_create.html'

    def get(self, request):
        form = NurseForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NurseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'Create', 'Created a new nurse')
            return redirect('nurse_list')
        return render(request, self.template_name, {'form': form})

class NurseUpdateView(View):
    template_name = 'nurse_update.html'

    def get(self, request, pk):
        nurse = get_object_or_404(Nurse, pk=pk)
        form = NurseForm(instance=nurse)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        nurse = get_object_or_404(Nurse, pk=pk)
        form = NurseForm(request.POST, request.FILES, instance=nurse)
        if form.is_valid():
            cleaned_email = form.cleaned_data['email']
            email_exists = CustomUser.objects.exclude(pk=nurse.user.pk).filter(email=cleaned_email).exists()
            if email_exists:
                form.add_error("email", "Email is not available, please use another email address...")
            else:
                form.save()
                log_activity(request.user, 'Update', f'Updated nurse with ID {nurse.pk}')
                return redirect('nurse_list')
        return render(request, self.template_name, {'form': form})

class NurseDeleteView(DeleteView):
    model = Nurse
    template_name = 'nurse_confirm_delete.html'
    success_url = reverse_lazy('nurse_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted nurse with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

class UserProfileView(View):
    template_name = 'user_profile.html'
    
    def get(self, request):

        user = self.request.user
        if request.user != user:
            messages.error(request, "You are not authorized to view this profile.")
            return redirect('home')

        employee = Employee.objects.filter(user=self.request.user)

        activities = Activity.objects.filter(user=user).order_by('-timestamp')
        return render(request, self.template_name, {'user_profile': user, 'activities': activities, 'user_form': CustomUserForm(instance=self.request.user), 'employee_form': EmployeeForm(instance=employee)})


class PharmacistListView(ListView):
    model = Pharmacist
    template_name = 'pharmacist_list.html'
    context_object_name = 'pharmacists'


class PharmacistDetailView(DetailView):
    model = Pharmacist
    template_name = 'pharmacist_detail.html'
    context_object_name = 'object'


class PharmacistCreateView(CreateView):
    model = Pharmacist
    form_class = PharmacistForm
    template_name = 'pharmacist_form.html'
    success_url = reverse_lazy('pharmacist-list')  # Ensure this URL is correct

    def get_success_url(self):
        # Customize success URL if needed
        return self.success_url  # Ensure this is not returning None

    def form_invalid(self, form):
        # Debug output for invalid form
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)
    

class PharmacistUpdateView(UpdateView):
    model = Pharmacist
    form_class = PharmacistForm
    template_name = 'pharmacist_form.html'
    success_url = reverse_lazy('pharmacist-list')


class PharmacistDeleteView(DeleteView):
    model = Pharmacist
    template_name = 'pharmacist_confirm_delete.html'
    success_url = reverse_lazy('pharmacist-list')
    
    
class LabTechnicianListView(ListView):
    model = LabTechnician
    template_name = 'lab_technician_list.html'
    context_object_name = 'lab_technicians'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context here if needed
        return context


class LabTechnicianCreateView(CreateView):
    model = LabTechnician
    form_class = LabTechnicianForm
    template_name = 'lab_technician_form.html'
    success_url = reverse_lazy('lab_technician_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Send a notification when a new Lab Technician is created
        Notification.objects.create(
            recipient=self.request.user,
            message=f"New Lab Technician {self.object.employee.user.get_full_name()} has been created."
        )
        messages.success(self.request, "Lab Technician created successfully.")
        return response


class LabTechnicianUpdateView(UpdateView):
    model = LabTechnician
    form_class = LabTechnicianForm
    template_name = 'lab_technician_form.html'
    success_url = reverse_lazy('lab_technician_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Send a notification when a Lab Technician is updated
        Notification.objects.create(
            recipient=self.request.user,
            message=f"Lab Technician {self.object.employee.user.get_full_name()} has been updated."
        )
        messages.success(self.request, "Lab Technician updated successfully.")
        return response


class LabTechnicianDeleteView(DeleteView):
    model = LabTechnician
    template_name = 'lab_technician_confirm_delete.html'
    success_url = reverse_lazy('lab_technician_list')

    def delete(self, request, *args, **kwargs):
        lab_technician = self.get_object()
        # Send a notification when a Lab Technician is deleted
        Notification.objects.create(
            user=request.user,
            content=f"Lab Technician {lab_technician.employee.user.get_full_name()} has been deleted."
        )
        messages.success(request, "Lab Technician deleted successfully.")
        return super().delete(request, *args, **kwargs)


class LabTechnicianDetailView(DetailView):
    model = LabTechnician
    template_name = 'lab_technician_detail.html'  # Template name
    context_object_name = 'lab_technician'        # Context variable name

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Add additional context if needed
        return context
    
    
class CaseManagerListView(LoginRequiredMixin, ListView):
    model = CaseManager
    template_name = 'case_manager_list.html'
    context_object_name = 'case_managers'

    def get_queryset(self):
        return CaseManager.objects.all()

class CaseManagerCreateView(LoginRequiredMixin, CreateView):
    model = CaseManager
    form_class = CaseManagerForm
    template_name = 'case_manager_form.html'
    success_url = reverse_lazy('case_manager_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log activity
        Activity.objects.create(
            user=self.request.user,
            action='create',
            description=f'Created Case Manager: {form.instance.employee.user.get_full_name()}',
            timestamp=timezone.now()
        )
        messages.success(self.request, 'Case Manager created successfully!')
        return response

class CaseManagerDetailView(LoginRequiredMixin, DetailView):
    model = CaseManager
    template_name = 'case_manager_detail.html'
    context_object_name = 'case_manager'

    def get_object(self):
        return CaseManager.objects.get(pk=self.kwargs.get('pk'))

class CaseManagerUpdateView(LoginRequiredMixin, UpdateView):
    model = CaseManager
    form_class = CaseManagerForm
    template_name = 'case_manager_form.html'
    success_url = reverse_lazy('case_manager_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log activity
        Activity.objects.create(
            user=self.request.user,
            action='update',
            description=f'Updated Case Manager: {form.instance.employee.user.get_full_name()}',
            timestamp=timezone.now()
        )
        messages.success(self.request, 'Case Manager updated successfully!')
        return response
    
    
class AccountantListView(LoginRequiredMixin, ListView):
    model = Accountant
    template_name = 'accountant_list.html'
    context_object_name = 'accountants'
    
    def get_queryset(self):
        return Accountant.objects.all()

class AccountantCreateView(LoginRequiredMixin, CreateView):
    model = Accountant
    form_class = AccountantForm
    template_name = 'accountant_form.html'
    success_url = reverse_lazy('accountant_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Activity.objects.create(
            user=self.request.user,
            action='create',
            description=f"Created Accountant {self.object.employee.user.get_full_name()}",
        )
        return response

class AccountantUpdateView(LoginRequiredMixin, UpdateView):
    model = Accountant
    form_class = AccountantForm
    template_name = 'accountant_form.html'
    success_url = reverse_lazy('accountant_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Activity.objects.create(
            user=self.request.user,
            action='update',
            description=f"Updated Accountant {self.object.employee.user.get_full_name()}",
        )
        return response

class AccountantDetailView(LoginRequiredMixin, DetailView):
    model = Accountant
    template_name = 'accountant/accountant_detail.html'
    context_object_name = 'accountant'

class AccountantDeleteView(LoginRequiredMixin, DeleteView):
    model = Accountant
    template_name = 'accountant/accountant_confirm_delete.html'
    success_url = reverse_lazy('accountant_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        Activity.objects.create(
            user=self.request.user,
            action='delete',
            description=f"Deleted Accountant {self.object.employee.user.get_full_name()}",
        )
        return response
    

class DischargeSummaryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DischargeSummary
    template_name = 'discharge_summary_list.html'
    context_object_name = 'discharge_summaries'
    permission_required = 'accounts.view_dischargesummary'

class DischargeSummaryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DischargeSummary
    template_name = 'discharge_summary_detail.html'
    context_object_name = 'discharge_summary'
    permission_required = 'accounts.view_dischargesummary'

class DischargeSummaryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DischargeSummary
    form_class = DischargeSummaryForm
    template_name = 'discharge_summary_form.html'
    success_url = reverse_lazy('discharge_summary_list')
    permission_required = 'accounts.add_dischargesummary'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created discharge summary for patient ID {self.object.patient.pk}')
        return response

class DischargeSummaryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DischargeSummary
    form_class = DischargeSummaryForm
    template_name = 'discharge_summary_form.html'
    success_url = reverse_lazy('discharge_summary_list')
    permission_required = 'accounts.change_dischargesummary'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated discharge summary for patient ID {self.object.patient.pk}')
        return response

class DischargeSummaryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DischargeSummary
    template_name = 'discharge_summary_confirm_delete.html'
    success_url = reverse_lazy('discharge_summary_list')
    permission_required = 'accounts.delete_dischargesummary'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted discharge summary for patient ID {self.object.patient.pk}')
        return super().delete(request, *args, **kwargs)
