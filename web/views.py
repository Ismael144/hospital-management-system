from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from messaging.models import Message
from accounts.models import Patient, Doctor, Nurse

User = get_user_model()

def get_user_role(user):
    # Example: Replace this logic with however roles are stored in your system
    if user.role.lower == 'doctor':
        return 'doctor'
    elif user.role.lower == 'nurse':
        return 'nurse'
    elif user.role.lower == 'case_manager':
        return 'case_manager'
    elif user.role.lower == 'laboratorist':
        return 'laboratorist'
    elif user.role.lower == 'pharmacist':
        return 'pharmacist'
    elif user.role.lower == 'receptionist':
        return 'receptionist'
    elif user.role.lower == 'patient':
        return 'patient'
    return None


class SignInRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('signin_page')


@login_required
def dashboard_view(request):
    user = request.user
    
    context = {}

    if user.role.lower() == 'doctor':
        assigned_doctor = Doctor.objects.filter(employee__user=request.user).first()
        context = {
            'appointments': Appointment.objects.filter(employee__user=request.user),
            'appointment_count': Appointment.objects.count(),
            'new_messages_count': Message.objects.filter(read=False).count(),
            'assigned_patients_count': Patient.objects.filter(status='New Patient', assigned_doctor=assigned_doctor)
        }
        
        return render(request, 'doctor_dashboard.html', context)
    
    elif user.role.lower() == 'nurse':
        return render(request, 'dashboards/nurse_dashboard.html')
    
    elif user.role.lower() == 'case_manager':
        return render(request, 'dashboards/case_manager_dashboard.html')
    
    elif user.role.lower() == 'laboratorist':
        return render(request, 'dashboards/laboratorist_dashboard.html')
    
    elif user.role.lower() == 'pharmacist':
        return render(request, 'dashboards/pharmacist_dashboard.html')
    
    elif user.role.lower() == 'receptionist':
        return render(request, 'dashboards/receptionist_dashboard.html')
    
    elif user.role.lower() == 'patient':
        return render(request, 'dashboards/patient_dashboard.html')
    
    # Optionally redirect to a default page or raise a 404 if role is not found
    return render(request, 'doctor_dashboard.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                
                    # Optionally redirect to a default page or raise a 404 if role is not found
                    return redirect('dashboard_page')
                else:
                    messages.error(request, "Invalid email password combination.")
                    return render(request, 'auth_login.html', {'error': 'Invalid email or password'})
            except User.DoesNotExist as e:
                print("Error: ", e)
                messages.error(request, "Invalid email password combination.")
                return render(request, 'auth_login.html', {'error': 'Invalid email or password'})
        else:
            messages.error(request, "Invalid email password combination.")
            return render(request, 'auth_login.html', {'error': 'Please enter both email and password'})
            
    return render(request, 'auth_login.html')


def logout_view(request): 
    logout(request)
    messages.success(request, "You logged out successfuly")
    return redirect('signin_page')