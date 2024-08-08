from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages 
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse 


class SignInRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('signin_page')


class DashboardView(SignInRequiredMixin, View): 
    def get(self, request): 
        # Bring in the notifications and messages
        messages.success(request, "Hello world")
        return render(request, "index6.html", {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'Admin':
                return redirect(reverse('dashboard_page'))
            elif user.role == 'Doctor':
                return redirect(reverse('dashboard_page'))
            elif user.role == 'Nurse':
                return redirect(reverse('dashboard_page'))
            elif user.role == 'Patient':
                return redirect(reverse('dashboard_page'))
            elif user.role == 'Receptionist':
                return redirect(reverse('dashboard_page'))
        else:
            messages.error(request, 'Invalid username or password')
            
    return render(request, 'auth_login.html')

