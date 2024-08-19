from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Attendance
from activities.models import Activity
from .forms import AttendanceForm, AttendanceSearchForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required

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



# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Count
# from django.utils import timezone
# from .models import Attendance

# @login_required
# def attendance_analysis(request):
#     # Get filter parameters
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     role = request.GET.get('role')

#     # Base queryset
#     queryset = Attendance.objects.all()

#     # Apply filters
#     if start_date:
#         queryset = queryset.filter(date__gte=start_date)
#     if end_date:
#         queryset = queryset.filter(date__lte=end_date)
#     if role:
#         queryset = queryset.filter(role=role)

#     # Generate role data
#     role_data = queryset.values('role').annotate(count=Count('id'))

#     # Generate status data
#     status_data = queryset.values('status').annotate(count=Count('id'))

#     # Generate date data
#     date_data = queryset.values('date').annotate(count=Count('id')).order_by('date')

#     context = {
#         'role_data': list(role_data),
#         'status_data': list(status_data),
#         'date_data': [{'date': item['date'].isoformat(), 'count': item['count']} for item in date_data],
#         'roles': Attendance.ROLE_CHOICES,
#         'start_date': start_date or '',
#         'end_date': end_date or '',
#         'selected_role': role or '',
#     }

#     return render(request, 'attendance_analysis.html', context)


from datetime import date, timedelta
import random

@login_required
def attendance_analysis(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    role = request.GET.get('role')

    # Generate dummy data
    roles = ['doctor', 'nurse', 'receptionist', 'patient']
    statuses = ['present', 'absent']
    
    # Use the filter dates if provided, otherwise use default range
    if start_date:
        start_date = date.fromisoformat(start_date)
    else:
        start_date = date(2024, 1, 1)
    
    if end_date:
        end_date = date.fromisoformat(end_date)
    else:
        end_date = date(2024, 12, 31)

    # Generate role data
    role_data = [
        {'role': r, 'count': random.randint(50, 200)}
        for r in roles if not role or r == role
    ]

    # Generate status data
    status_data = [
        {'status': status, 'count': random.randint(100, 300)}
        for status in statuses
    ]

    # Generate date data
    date_data = [
        {
            'date': (start_date + timedelta(days=i)).isoformat(),
            'count': random.randint(10, 50)
        }
        for i in range((end_date - start_date).days + 1)
    ]

    context = {
        'role_data': role_data,
        'status_data': status_data,
        'date_data': date_data,
        'roles': [('doctor', 'Doctor'), ('nurse', 'Nurse'), ('receptionist', 'Receptionist'), ('patient', 'Patient')],
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'selected_role': role,
        'start_date': request.GET.get('start_date'), 
        'end_date': request.GET.get('end_date'), 
        'role': role
    }

    return render(request, 'attendance_analysis.html', context)
