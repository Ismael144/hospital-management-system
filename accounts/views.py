from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib import messages
from .models import Receptionist, Patient, Doctor, Nurse, CustomUser, DischargeSummary, Pharmacist, LabTechnician, CaseManager, Accountant, MedicalReport
from activities.models import Activity
from .forms import PatientForm, DoctorForm, NurseForm, CustomUserForm, ReceptionistForm, DischargeSummaryForm, PharmacistForm, LabTechnicianForm, CaseManagerForm, AccountantForm
from messaging.models import Notification 
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Employee
from .forms import EmployeeForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import DischargeSummary, Patient
from django.db.models import Case, When, Value, CharField, Count
from financials.models import Payment, Bill
from pharmacy.models import Prescription
from appointments.models import Appointment
from django.core.exceptions import ValidationError
from .forms import MedicalReportForm

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
    

@login_required(login_url="/signin")
def comprehensive_analysis(request):
    # Time range for analysis
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)  # Last 30 days

    # Discharge Summary Analysis
    discharge_summary = DischargeSummary.objects.filter(discharge_date__range=[start_date, end_date])
    discharge_status = discharge_summary.values('discharge_status').annotate(count=Count('id'))
    discharge_reasons = discharge_summary.values('discharge_reason').annotate(count=Count('id'))[:5]

    # Patient Analysis
    patients = Patient.objects.all()
    patient_status = patients.values('status').annotate(count=Count('id'))
    age_groups = patients.annotate(
        age_group=Case(
            When(date_of_birth__gte=timezone.now().date() - timedelta(days=365*18), then=Value('0-18')),
            When(date_of_birth__gte=timezone.now().date() - timedelta(days=365*30), then=Value('19-30')),
            When(date_of_birth__gte=timezone.now().date() - timedelta(days=365*50), then=Value('31-50')),
            default=Value('51+'),
            output_field=CharField(),
        )
    ).values('age_group').annotate(count=Count('id'))

    # Payment and Bill Analysis
    payments = Payment.objects.filter(date_paid__range=[start_date, end_date])
    payment_methods = payments.values('payment_method').annotate(count=Count('id'), total=Sum('amount'))
    bills = Bill.objects.filter(date_issued__range=[start_date, end_date])
    bill_status = bills.values('status').annotate(count=Count('id'), total=Sum('total_amount'))
    insurance_claims = bills.values('insurance_claim_status').annotate(count=Count('id'))

    # Prescription Analysis
    prescriptions = Prescription.objects.filter(issue_date__range=[start_date, end_date])
    top_medications = prescriptions.values('medication__name').annotate(count=Count('id'))[:10]

    # Appointment Analysis
    appointments = Appointment.objects.filter(appointment_date__range=[start_date, end_date])
    appointment_status = appointments.values('status').annotate(count=Count('id'))
    appointments_by_day = appointments.values('appointment_date__date').annotate(count=Count('id')).order_by('appointment_date__date')

    context = {
        'discharge_status': list(discharge_status),
        'discharge_reasons': list(discharge_reasons),
        'patient_status': list(patient_status),
        'age_groups': list(age_groups),
        'payment_methods': list(payment_methods),
        'bill_status': list(bill_status),
        'insurance_claims': list(insurance_claims),
        'top_medications': list(top_medications),
        'appointment_status': list(appointment_status),
        'appointments_by_day': list(appointments_by_day),
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'comprehensive_analysis.html', context)


class PatientUpdateView(View, SignInRequiredMixin):
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

        employee = Employee.objects.filter(user=user).first()
        print("Employee: ", employee)

        is_employee = True if employee is not None else False

        activities = Activity.objects.filter(user=user).order_by('-timestamp')
        return render(request, self.template_name, {'user_profile': user, 'activities': activities, 'user_form': CustomUserForm(instance=self.request.user), 'employee_form': EmployeeForm(instance=employee), 'is_employee': is_employee, 'employee': employee})


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
    
    
class CaseManagerListView(SignInRequiredMixin, ListView):
    model = CaseManager
    template_name = 'case_manager_list.html'
    context_object_name = 'case_managers'

    def get_queryset(self):
        return CaseManager.objects.all()


class CaseManagerCreateView(SignInRequiredMixin, CreateView):
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


class CaseManagerDetailView(SignInRequiredMixin, DetailView):
    model = CaseManager
    template_name = 'case_manager_detail.html'
    context_object_name = 'case_manager'

    def get_object(self):
        return CaseManager.objects.get(pk=self.kwargs.get('pk'))


class CaseManagerUpdateView(SignInRequiredMixin, UpdateView):
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
    
    
class AccountantListView(SignInRequiredMixin, ListView):
    model = Accountant
    template_name = 'accountant_list.html'
    context_object_name = 'accountants'
    
    def get_queryset(self):
        return Accountant.objects.all()


class AccountantCreateView(SignInRequiredMixin, CreateView):
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


class AccountantUpdateView(SignInRequiredMixin, UpdateView):
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

class AccountantDetailView(SignInRequiredMixin, DetailView):
    model = Accountant
    template_name = 'accountant/accountant_detail.html'
    context_object_name = 'accountant'

class AccountantDeleteView(SignInRequiredMixin, DeleteView):
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
    

class DischargeSummaryListView(SignInRequiredMixin, PermissionRequiredMixin, ListView):
    model = DischargeSummary
    template_name = 'discharge_summary_list.html'
    context_object_name = 'discharge_summaries'
    permission_required = 'accounts.view_dischargesummary'
    
 

    def get_queryset(self):
        discharge_summaries = super().get_queryset()
        
        patient_id = self.request.GET.get('patient')
        
        if patient_id:
            try:
                # Validate that patient_id is an integer
                patient_id = int(patient_id)
                # Fetch the patient object safely
                patient = get_object_or_404(Patient, pk=patient_id)
                discharge_summaries = discharge_summaries.filter(patient=patient)
            except (ValueError, ValidationError):
                # Handle the case where patient_id is not a valid integer
                discharge_summaries = discharge_summaries.none()
        
        return discharge_summaries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        
        patient_id = self.request.GET.get('patient')
        if patient_id:
            try:
                patient_id = int(patient_id)
                context['selected_patient'] = Patient.objects.filter(pk=patient_id).first()
            except (ValueError, ValidationError):
                context['selected_patient'] = None
        
        return context
 
 
class DischargeSummaryDetailView(SignInRequiredMixin, PermissionRequiredMixin, DetailView):
    model = DischargeSummary
    template_name = 'discharge_summary_detail.html'
    context_object_name = 'discharge_summary'
    permission_required = 'accounts.view_dischargesummary'


class DischargeSummaryCreateView(SignInRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DischargeSummary
    form_class = DischargeSummaryForm
    template_name = 'discharge_summary_form.html'
    success_url = reverse_lazy('discharge_summary_list')
    permission_required = 'accounts.add_dischargesummary'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created discharge summary for patient ID {self.object.patient.pk}')
        return response


class DischargeSummaryUpdateView(SignInRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DischargeSummary
    form_class = DischargeSummaryForm
    template_name = 'discharge_summary_form.html'
    success_url = reverse_lazy('discharge_summary_list')
    permission_required = 'accounts.change_dischargesummary'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated discharge summary for patient ID {self.object.patient.pk}')
        return response


class DischargeSummaryDeleteView(SignInRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DischargeSummary
    template_name = 'discharge_summary_confirm_delete.html'
    success_url = reverse_lazy('discharge_summary_list')
    permission_required = 'accounts.delete_dischargesummary'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted discharge summary for patient ID {self.object.patient.pk}')
        return super().delete(request, *args, **kwargs)


class MedicalReportListView(SignInRequiredMixin, ListView):
    model = MedicalReport
    template_name = 'medical_report_list.html'
    context_object_name = 'medical_reports'

    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.GET.get('patient')
        
        if patient_id:
            patient = get_object_or_404(Patient, pk=patient_id)
            queryset = queryset.filter(patient=patient)

        return queryset

    def get_context_data(self, **kwargs): 
        context_data = super().get_context_data()
        context_data['patients'] = Patient.objects.all()
        patient_id = self.request.GET.get('patient')

        if patient_id: 
            patient = get_object_or_404(Patient, pk=patient_id)
            context_data['selected_patient'] = patient

        return context_data

class MedicalReportDetailView(SignInRequiredMixin, DetailView):
    model = MedicalReport
    template_name = 'medical_report_detail.html'
    context_object_name = 'medical_report'

class MedicalReportCreateView(SignInRequiredMixin, CreateView):
    model = MedicalReport
    form_class = MedicalReportForm
    template_name = 'medical_report_form.html'
    success_url = reverse_lazy('medical_report_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'create', f"Created Medical Report for patient {self.object.patient} on {self.object.date_of_examination}")
        return response

class MedicalReportUpdateView(SignInRequiredMixin, UpdateView):
    model = MedicalReport
    form_class = MedicalReportForm
    template_name = 'medical_report_form.html'
    success_url = reverse_lazy('medical_report_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'update', f"Updated Medical Report for patient {self.object.patient} on {self.object.date_of_examination}")
        return response

class MedicalReportDeleteView(SignInRequiredMixin, DeleteView):
    model = MedicalReport
    template_name = 'medical_report_confirm_delete.html'
    success_url = reverse_lazy('medical_report_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'delete', f"Deleted Medical Report for patient {self.object.patient} on {self.object.date_of_examination}")
        return super().delete(request, *args, **kwargs)