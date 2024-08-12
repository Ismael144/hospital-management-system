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
        user = authenticate(request, email=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard_page'))
            
    return render(request, 'auth_login.html')

