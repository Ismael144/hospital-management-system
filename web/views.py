from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages 
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

User = get_user_model()

class SignInRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('signin_page')


class DashboardView(SignInRequiredMixin, View): 
    def get(self, request): 
        # Bring in the notifications and messages
        messages.success(request, "Hello world")
        return render(request, "index6.html", {})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    return redirect(reverse('dashboard_page'))
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