from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Appointment
from activities.models import Activity
from .forms import AppointmentForm, AppointmentUpdateForm
from mixins import DetailViewMixin
from messaging.helpers import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from accounts.models import Patient, Doctor, Employee, Nurse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)


@method_decorator([login_required, permission_required('appointments.view_appointment', raise_exception=True)], name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        # Filter appointments based on the user's role
        if user.role == 'patient':
            # Show appointments for the logged-in patient
            return Appointment.objects.filter(patient__user=user)
        elif user.role == 'doctor':
            # Show appointments for the logged-in doctor
            return Appointment.objects.filter(doctor__employee__user=user)
        elif user.role == 'nurse':
            # Show appointments for the logged-in nurse
            return Appointment.objects.filter(nurse__employee__user=user)
        else:
            # Default behavior: show all appointments (admin or other roles)
            return Appointment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context
    
    def post(self, request, *args, **kwargs):
        request_data = request.POST
        appt_id = request_data.get('appt_id') 
        cancellation_reason = str(request_data.get('cancellation_reason')).strip()

        if appt_id is not None:
            # Process the cancellation here
            print(f"Appointment ID: {appt_id}, Cancellation Reason: {cancellation_reason}")
            # Add your cancellation logic here
            appointment = Appointment.objects.filter(pk=appt_id)[0]
            print(appointment)
            
            # Do some form validations here 
            if cancellation_reason == '': 
                messages.error(request, "A cancellation reason is needed in order to cancel appointment")
                return self.get(request, *args, **kwargs)

            if len(cancellation_reason) < 10: 
                messages.error(request, "The cancellation reason should be meaningful and long enough")
                return self.get(request, *args, **kwargs)

            # Checking whether eiher doctor or nurse is not None
            med = appointment.doctor if appointment.doctor is not None else appointment.nurse

            if appointment is None:
                messages.info(request, "An error occured, please try again!")
                return self.get(request, *args, **kwargs)
            
            if med.employee.user == request.user or appointment.patient.user == request.user: 
                appointment.cancellation_reason = cancellation_reason
                appointment.status = "Cancelled"
                appointment.is_cancelled = True
                appointment.save()
                
                title = "Nr." if isinstance(med, Nurse) else "Dr." 
                
                # Send Notifications to patient and (doctor or nurse)
                send_notification(
                    user=appointment.patient.user,
                    content=f'Your appointment with {title} {med.employee.user.get_full_name()} has been updated',
                    icon='fa-calendar-alt',
                    link=reverse('appointment_detail', args=[appointment.pk]),
                    link_name='View Updated Appointment',
                    bg_color='danger'
                )
                
                send_notification(
                    user=med.employee.user,
                    content=f'Your appointment with {appointment.patient.user.get_full_name()} has been updated',
                    icon='fa-calendar-alt',
                    link=reverse('appointment_detail', args=[appointment.pk]),
                    link_name='View Updated Appointment',
                    bg_color='danger'
                )
                
            else: 
                messages.error(request, "You have not rights of cancelling this appointment")
                return self.get(request, *args, **kwargs)

        return self.get(request, *args, **kwargs)
    

@method_decorator([login_required, permission_required('appointments.view_appointment', raise_exception=True)], name='dispatch')
class AppointmentDetailView(DetailViewMixin, DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            raise Http404("You must be logged in to view appointment details.")

        if user.is_superuser or user.role.lower() in ['admin', 'receptionist']:
            return queryset  # Admins and receptionists can see all appointments

        role = user.role.lower()

        if role == 'patient':
            patient = get_object_or_404(Patient, user=user)
            return queryset.filter(patient=patient)

        elif role in ['doctor', 'nurse']:
            employee = get_object_or_404(Employee, user=user)
            if role == 'doctor':
                doctor = get_object_or_404(Doctor, employee=employee)
                return queryset.filter(doctor=doctor)
            else:  # nurse
                return queryset.filter(nurse=employee)

        else:
            raise Http404("You don't have permission to view this appointment.")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj not in self.get_queryset():
            raise Http404("You don't have permission to view this appointment.")
        return obj
    

# Appointment views
@method_decorator([login_required, permission_required('appointments.add_appointment', raise_exception=True)], name='dispatch')
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new appointment with ID {self.object.pk}')
        
        # Send notifications
        appointment = self.object
        patient = appointment.patient
        med = appointment.doctor if appointment.doctor is not None else appointment.nurse
        title = "Nr." if isinstance(med, Nurse) else "Dr." 

        send_notification(
            user=patient.user,
            content=f'You have a new appointment with {title} {med.employee.user.get_full_name()}',
            icon='fa-calendar-alt',
            link=reverse('appointment_detail', args=[appointment.pk]),
            link_name='View Appointment',
            bg_color='success'
        )
        
        send_notification(
            user=med.employee.user,
            content=f'You have a new appointment with {patient.user.get_full_name()}',
            icon='fa-calendar-alt',
            link=reverse('appointment_detail', args=[appointment.pk]),
            link_name='View Appointment',
            bg_color='success'
        )

        return response
    
    
@method_decorator([login_required, permission_required('appointments.change_appointment', raise_exception=True)], name='dispatch')
class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentUpdateForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated appointment with ID {self.object.pk}')
        
        # Send notifications
        appointment = self.object
        patient = appointment.patient
        med = appointment.doctor if appointment.doctor is not None else appointment.nurse
        title = "Nr." if isinstance(med, Nurse) else "Dr." 


        send_notification(
            user=patient.user,
            content=f'Your appointment with {title} {med.employee.user.get_full_name()} has been updated',
            icon='fa-calendar-alt',
            link=reverse('appointment_detail', args=[appointment.pk]),
            link_name='View Updated Appointment',
            bg_color='success'
        )
        
        send_notification(
            user=med.employee.user,
            content=f'Your appointment with {title} {patient.user.get_full_name()} has been updated',
            icon='fa-calendar-alt',
            link=reverse('appointment_detail', args=[appointment.pk]),
            link_name='View Updated Appointment',
            bg_color='success'
        )

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        
        # Access the doctor and patient
        context['is_updating'] = True 
        context['doctor'] = appointment.doctor
        context['patient'] = appointment.patient
        
        return context

class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted appointment with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)
