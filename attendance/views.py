from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Attendance
from activities.models import Activity
from .forms import AttendanceForm, AttendanceSearchForm
from django.urls import reverse_lazy
from django.contrib import messages

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance_list.html'
    context_object_name = 'attendances'

class AttendanceDetailView(DetailView):
    model = Attendance
    template_name = 'attendance_detail.html'
    context_object_name = 'attendance'

class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance_form.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new attendance record with ID {self.object.pk}')
        return response

class AttendanceUpdateView(UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance_form.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated attendance record with ID {self.object.pk}')
        return response

def search_attendance(request):
    form = AttendanceSearchForm()
    attendance_records = None
    
    if request.method == 'POST':
        form = AttendanceSearchForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            date = form.cleaned_data['date']
            attendance_records = Attendance.objects.filter(user=user, date=date)
            
            # Log search activity
            log_activity(request.user, 'Search', f'Searched for attendance records for user {user} on {date}')
    
    context = {
        'form': form,
        'attendance_records': attendance_records,
    }
    return render(request, 'attendance_search.html', context)
