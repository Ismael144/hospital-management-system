from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Schedule, StaffOnDuty, NoticeBoard, Department
from .forms import ScheduleForm, StaffOnDutyForm, NoticeBoardForm
from mixins import *
from .forms import *
from messaging.models import Notification 

# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'financials/department_list.html'
    context_object_name = 'staff_management/departments'

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'financials/department_detail.html'

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    template_name = 'financials/department_form.html'
    fields = ['name', 'code', 'description', 'head', 'is_active']
    success_url = reverse_lazy('department-list')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    template_name = 'financials/department_form.html'
    fields = ['name', 'code', 'description', 'head', 'is_active']
    success_url = reverse_lazy('department-list')

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'financials/department_confirm_delete.html'
    success_url = reverse_lazy('department-list')


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedules/schedule_list.html'
    context_object_name = 'schedules'

class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedules/schedule_form.html'
    success_url = reverse_lazy('schedule_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Schedule "{form.instance.title}" created successfully.',
            link=self.get_success_url(),
            icon='fa fa-calendar-plus'
        )
        return response

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'schedules/schedule_form.html'
    success_url = reverse_lazy('schedule_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Schedule "{form.instance.title}" updated successfully.',
            link=self.get_success_url(),
            icon='fa fa-calendar-edit'
        )
        return response

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    template_name = 'schedules/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        Notification.objects.create(
            user=self.request.user,
            message=f'Schedule "{self.object.title}" deleted successfully.',
            link=self.success_url,
            icon='fa fa-calendar-times'
        )
        return response


class NoticeBoardListView(ListView):
    model = NoticeBoard
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'

class NoticeBoardDetailView(DetailView):
    model = NoticeBoard
    template_name = 'notices/notice_detail.html'
    context_object_name = 'notice'

class NoticeBoardCreateView(LoginRequiredMixin, CreateView):
    model = NoticeBoard
    form_class = NoticeBoardForm
    template_name = 'staff_management/noticeboard_form.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Notice "{form.instance.title}" created successfully.',
            link=self.get_success_url(),
            icon='fa fa-bullhorn'
        )
        return response

class NoticeBoardUpdateView(LoginRequiredMixin, UpdateView):
    model = NoticeBoard
    form_class = NoticeBoardForm
    template_name = 'notices/notice_form.html'
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Notice "{form.instance.title}" updated successfully.',
            link=self.get_success_url(),
            icon='fa fa-edit'
        )
        return response

class NoticeBoardDeleteView(LoginRequiredMixin, DeleteView):
    model = NoticeBoard
    template_name = 'notices/notice_confirm_delete.html'
    success_url = reverse_lazy('notice_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        Notification.objects.create(
            user=self.request.user,
            message=f'Notice "{self.object.title}" deleted successfully.',
            link=self.success_url,
            icon='fa fa-trash'
        )
        return response



class StaffOnDutyListView(ListView):
    model = StaffOnDuty
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_on_duty'

class StaffOnDutyDetailView(DetailView):
    model = StaffOnDuty
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'

class StaffOnDutyCreateView(LoginRequiredMixin, CreateView):
    model = StaffOnDuty
    form_class = StaffOnDutyForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Staff "{form.instance.name}" is on duty.',
            link=self.get_success_url(),
            bg_color="success",
            icon='fa fa-user-plus'
        )
        return response

class StaffOnDutyUpdateView(LoginRequiredMixin, UpdateView):
    model = StaffOnDuty
    form_class = StaffOnDutyForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Staff "{form.instance.name}" updated successfully.',
            link=self.get_success_url(),
            icon='fa fa-user-edit'
        )
        return response

class StaffOnDutyDeleteView(LoginRequiredMixin, DeleteView):
    model = StaffOnDuty
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        Notification.objects.create(
            user=self.request.user,
            message=f'Staff "{self.object.name}" removed from duty successfully.',
            link=self.success_url,
            icon='fa fa-user-times'
        )
        return response


class ShiftListView(LoginRequiredMixin, ListView):
    model = Shift
    template_name = 'staff_management/shifts/shift_list.html'
    context_object_name = 'shifts'

class ShiftCreateView(LoginRequiredMixin, CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'staff_management/shifts/shift_form.html'
    success_url = reverse_lazy('shift_list')

class ShiftUpdateView(LoginRequiredMixin, UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'staff_management/shifts/shift_form.html'
    success_url = reverse_lazy('shift_list')

class ShiftDeleteView(DeleteView):
    model = Shift
    template_name = 'shift_confirm_delete.html'
    success_url = reverse_lazy('shift_list')

# Department Views

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'staff_management/departments/department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'staff_management/departments/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'staff_management/departments/department_form.html'
    success_url = reverse_lazy('department_list')