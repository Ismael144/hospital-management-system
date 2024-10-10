from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from activities.models import Activity
from messaging.models import Notification
from .models import Department, Schedule, StaffOnDuty, NoticeBoard, Shift
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ScheduleForm, StaffOnDutyForm, NoticeBoardForm, ShiftForm, DepartmentForm, LeaveForm
from django.contrib import messages 
from django.shortcuts import redirect, get_object_or_404


def log_activity(user, action, description=''):
    Activity.objects.create(user=user, action=action, description=description, timestamp=timezone.now())

# Department Views
@method_decorator([login_required, permission_required('human_resource.view_department', raise_exception=True)], name='dispatch')
class DepartmentListView(ListView):
    model = Department
    template_name = 'human_resource/departments/department_list.html'
    context_object_name = 'departments'

@method_decorator([login_required, permission_required('human_resource.view_department', raise_exception=True)], name='dispatch')
class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'human_resource/departments/department_detail.html'

@method_decorator([login_required, permission_required('human_resource.add_department', raise_exception=True)], name='dispatch')
class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'human_resource/departments/department_form.html'
    success_url = reverse_lazy('department_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Created Department', f'Department "{form.instance.name}" created successfully.')
        return response

@method_decorator([login_required, permission_required('human_resource.change_department', raise_exception=True)], name='dispatch')
class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'human_resource/departments/department_form.html'
    success_url = reverse_lazy('department_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Updated Department', f'Department "{form.instance.name}" updated successfully.')
        return response

@method_decorator([login_required, permission_required('human_resource.delete_department', raise_exception=True)], name='dispatch')
class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'human_resource/departments/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        log_activity(self.request.user, 'Deleted Department', f'Department "{self.object.name}" deleted successfully.')
        return response

# Schedule Views
@method_decorator([login_required, permission_required('schedules.view_schedule', raise_exception=True)], name='dispatch')
class ScheduleListView(ListView):
    model = Schedule
    template_name = 'schedules/schedule_list.html'
    context_object_name = 'schedules'

@method_decorator([login_required, permission_required('schedules.view_schedule', raise_exception=True)], name='dispatch')
class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

@method_decorator([login_required, permission_required('schedules.add_schedule', raise_exception=True)], name='dispatch')
class ScheduleCreateView(CreateView):
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
        log_activity(self.request.user, 'Created Schedule', f'Schedule "{form.instance.title}" created successfully.')
        return response

@method_decorator([login_required, permission_required('schedules.change_schedule', raise_exception=True)], name='dispatch')
class ScheduleUpdateView(UpdateView):
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
        log_activity(self.request.user, 'Updated Schedule', f'Schedule "{form.instance.title}" updated successfully.')
        return response

@method_decorator([login_required, permission_required('schedules.delete_schedule', raise_exception=True)], name='dispatch')
class ScheduleDeleteView(DeleteView):
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
        log_activity(self.request.user, 'Deleted Schedule', f'Schedule "{self.object.title}" deleted successfully.')
        return response

# NoticeBoard Views
@method_decorator([login_required, permission_required('notices.view_noticeboard', raise_exception=True)], name='dispatch')
class NoticeBoardListView(ListView):
    model = NoticeBoard
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'

@method_decorator([login_required, permission_required('notices.view_noticeboard', raise_exception=True)], name='dispatch')
class NoticeBoardDetailView(DetailView):
    model = NoticeBoard
    template_name = 'human_resource/noticeboard_detail.html'
    context_object_name = 'notice'

@method_decorator([login_required, permission_required('notices.add_noticeboard', raise_exception=True)], name='dispatch')
class NoticeBoardCreateView(CreateView):
    model = NoticeBoard
    form_class = NoticeBoardForm
    template_name = 'human_resource/noticeboard_form.html'
    success_url = reverse_lazy('noticeboard_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.objects.create(
            user=self.request.user,
            message=f'Notice "{form.instance.title}" created successfully.',
            link=self.get_success_url(),
            icon='fa fa-bullhorn'
        )
        log_activity(self.request.user, 'Created NoticeBoard', f'Notice "{form.instance.title}" created successfully.')
        return response

@method_decorator([login_required, permission_required('notices.change_noticeboard', raise_exception=True)], name='dispatch')
class NoticeBoardUpdateView(UpdateView):
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
        log_activity(self.request.user, 'Updated NoticeBoard', f'Notice "{form.instance.title}" updated successfully.')
        return response

@method_decorator([login_required, permission_required('notices.delete_noticeboard', raise_exception=True)], name='dispatch')
class NoticeBoardDeleteView(DeleteView):
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
        log_activity(self.request.user, 'Deleted NoticeBoard', f'Notice "{self.object.title}" deleted successfully.')
        return response

# StaffOnDuty Views
@method_decorator([login_required, permission_required('human_resource.view_staffonduty', raise_exception=True)], name='dispatch')
class StaffOnDutyListView(ListView):
    model = StaffOnDuty
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_on_duty'

@method_decorator([login_required, permission_required('human_resource.view_staffonduty', raise_exception=True)], name='dispatch')
class StaffOnDutyDetailView(DetailView):
    model = StaffOnDuty
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'

@method_decorator([login_required, permission_required('human_resource.add_staffonduty', raise_exception=True)], name='dispatch')
class StaffOnDutyCreateView(CreateView):
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
        log_activity(self.request.user, 'Created StaffOnDuty', f'Staff "{form.instance.name}" is on duty.')
        return response

@method_decorator([login_required, permission_required('human_resource.change_staffonduty', raise_exception=True)], name='dispatch')
class StaffOnDutyUpdateView(UpdateView):
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
        log_activity(self.request.user, 'Updated StaffOnDuty', f'Staff "{form.instance.name}" updated successfully.')
        return response

@method_decorator([login_required, permission_required('human_resource.delete_staffonduty', raise_exception=True)], name='dispatch')
class StaffOnDutyDeleteView(DeleteView):
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
        log_activity(self.request.user, 'Deleted StaffOnDuty', f'Staff "{self.object.name}" removed from duty.')
        return response

# Shift Views
@method_decorator([login_required, permission_required('human_resource.view_shift', raise_exception=True)], name='dispatch')
class ShiftListView(ListView):
    model = Shift
    template_name = 'human_resource/shifts/shift_list.html'
    context_object_name = 'shifts'

@method_decorator([login_required, permission_required('human_resource.add_shift', raise_exception=True)], name='dispatch')
class ShiftCreateView(CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'human_resource/shifts/shift_form.html'
    success_url = reverse_lazy('shift_list')

@method_decorator([login_required, permission_required('human_resource.change_shift', raise_exception=True)], name='dispatch')
class ShiftUpdateView(UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'human_resource/shifts/shift_form.html'
    success_url = reverse_lazy('shift_list')

@method_decorator([login_required, permission_required('human_resource.delete_shift', raise_exception=True)], name='dispatch')
class ShiftDeleteView(DeleteView):
    model = Shift
    template_name = 'human_resource/shifts/shift_confirm_delete.html'
    success_url = reverse_lazy('shift_list')


# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'human_resource/departments/department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'human_resource/departments/department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'human_resource/departments/department_form.html'
    success_url = reverse_lazy('department_list')



class LeaveListView(ListView):
    model = Leave
    template_name = 'human_resource/leave_list.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        log_activity(self.request.user, 'view', 'Viewed Leave List')
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        leave = get_object_or_404(Leave, pk=request.POST.get('leave_id'))
        action = request.POST.get('action')
        
        if action == 'approved':
            leave.status = 'Approved'
            leave.save()
            send_notification(
                    user=leave.employee.user,
                    content=f'Your Leave request was successfuly approved by {leave.employee.user.get_full_name()}.', 
                    icon="fa-bell", 
                    link=f"/financials/leaves/{leave.pk}", 
                    link_name="View Leave", 
                    bg_color="success"
            )
            log_activity(self.request.user, 'approve', f'Approved leave request for {leave.employee.user.get_full_name}')
            messages.success(request, 'Leave request approved successfully.')

        elif action == 'reject':
            reason = request.POST.get('rejection_reason')
            if not reason:
                messages.error(request, 'Reason for rejection is required.')
                print("Reason not given")
                return redirect('leave_list')
            
            leave.status = 'Rejected'
            leave.rejection_reason = reason
            leave.save()
            send_notification(
                    user=leave.employee.user,
                    content=f'Your leave request was rejected.', 
                    icon="fa-bell", 
                    link=f"/financials/leaves/{leave.pk}", 
                    link_name="View Leave Request", 
                    bg_color="danger"
                )
            log_activity(self.request.user, 'reject', f'Rejected leave request for {leave.employee.user.get_full_name} with reason: {reason}')
            messages.success(request, 'Leave request rejected successfully.')
        
        return redirect('leave-list')

class LeaveDetailView(DetailView):
    model = Leave
    template_name = 'human_resource/leave_detail.html'
    context_object_name = 'leave'

    def get_object(self):
        log_activity(self.request.user, 'view', f"Viewed Leave: {self.kwargs['pk']}")
        return super().get_object()

class LeaveCreateView(CreateView):
    model = Leave
    template_name = 'human_resource/leave_form.html'
    form_class = LeaveForm
    success_url = reverse_lazy('leave-list')
    
    def form_valid(self, form):
        log_activity(self.request.user, 'create', f"Created Leave: {form.instance.employee} ({form.instance.leave_type})")
        send_notification(
            user=form.instance.employee.user,
            content=f'You successfully requested a pending leave.', 
            icon="fa-bell", 
            link=f"/financials/leaves/{form.instance.pk}", 
            link_name="View Leave", 
            bg_color="primary"
        )
        return super().form_valid(form)
    

class LeaveUpdateView(UpdateView):
    model = Leave
    template_name = 'human_resource/leave_form.html'
    form_class = LeaveForm

    def form_valid(self, form):
        log_activity(self.request.user, 'update', f"Updated Leave: {form.instance.employee} ({form.instance.leave_type})")
        return super().form_valid(form)

class LeaveDeleteView(DeleteView):
    model = Leave
    template_name = 'human_resource/leave_confirm_delete.html'
    success_url = reverse_lazy('leave-list')

    def delete(self, request, *args, **kwargs):
        leave = self.get_object()
        log_activity(self.request.user, 'delete', f"Deleted Leave: {leave.employee} ({leave.leave_type})")
        return super().delete(request, *args, **kwargs)


class PerformanceReviewListView(ListView):
    model = PerformanceReview
    template_name = 'performance_reviews/performance_review_list.html'

    def get_queryset(self):
        log_activity(self.request.user, 'view', 'Viewed Performance Review List')
        return super().get_queryset()

class PerformanceReviewDetailView(DetailView):
    model = PerformanceReview
    template_name = 'performance_reviews/performance_review_detail.html'

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        log_activity(self.request.user, 'view', f'Viewed Performance Review: {review}')
        return review

class PerformanceReviewCreateView(CreateView):
    model = PerformanceReview
    # template_name = 'performance_reviews/performance_review_form.html'
    fields = ['employee', 'reviewer', 'review_date', 'performance_score', 'comments', 'goals']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'create', f'Created Performance Review: {self.object}')
        return response

class PerformanceReviewUpdateView(UpdateView):
    model = PerformanceReview
    template_name = 'performance_reviews/performance_review_form.html'
    fields = ['employee', 'reviewer', 'review_date', 'performance_score', 'comments', 'goals']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'update', f'Updated Performance Review: {self.object}')
        return response

class PerformanceReviewDeleteView(DeleteView):
    model = PerformanceReview
    template_name = 'performance_reviews/performance_review_confirm_delete.html'
    success_url = reverse_lazy('performance-review-list')

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        response = super().delete(request, *args, **kwargs)
        log_activity(request.user, 'delete', f'Deleted Performance Review: {review}')
        return response


class TrainingListView(ListView):
    model = Training
    template_name = 'trainings/training_list.html'

    def get_queryset(self):
        log_activity(self.request.user, 'view', 'Viewed Training List')
        return super().get_queryset()

class TrainingDetailView(DetailView):
    model = Training
    template_name = 'human_resource/training_detail.html'

    def get_object(self, queryset=None):
        training = super().get_object(queryset)
        log_activity(self.request.user, 'view', f'Viewed Training: {training}')
        return training

class TrainingCreateView(CreateView):
    model = Training
    template_name = 'human_resource/training_form.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'trainer', 'participants']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'create', f'Created Training: {self.object}')
        return response

class TrainingUpdateView(UpdateView):
    model = Training
    template_name = 'human_resource/training_form.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'trainer']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'update', f'Updated Training: {self.object}')
        return response

class TrainingDeleteView(DeleteView):
    model = Training
    template_name = 'human_resource/training_confirm_delete.html'
    success_url = reverse_lazy('training-list')

    def delete(self, request, *args, **kwargs):
        training = self.get_object()
        response = super().delete(request, *args, **kwargs)
        log_activity(request.user, 'delete', f'Deleted Training: {training}')
        return response

class TrainingParticipantListView(ListView):
    model = TrainingParticipant
    template_name = 'human_resource/training_participant_list.html'

    def get_queryset(self):
        log_activity(self.request.user, 'view', 'Viewed Training Participant List')
        return super().get_queryset()

class TrainingParticipantDetailView(DetailView):
    model = TrainingParticipant
    template_name = 'human_resource/trainingparticipant_detail.html'

    def get_object(self, queryset=None):
        participant = super().get_object(queryset)
        log_activity(self.request.user, 'view', f'Viewed Training Participant: {participant}')
        return participant

class TrainingParticipantCreateView(CreateView):
    model = TrainingParticipant
    template_name = 'human_resource/trainingparticipant_form.html'
    fields = ['employee', 'training', 'completion_date', 'certificate_issued']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'create', f'Created Training Participant: {self.object}')
        return response

class TrainingParticipantUpdateView(UpdateView):
    model = TrainingParticipant
    template_name = 'human_resource/trainingparticipant_form.html'
    fields = ['employee', 'training', 'completion_date', 'certificate_issued']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'update', f'Updated Training Participant: {self.object}')
        return response

class TrainingParticipantDeleteView(DeleteView):
    model = TrainingParticipant
    template_name = 'training_participants/training_participant_confirm_delete.html'
    success_url = reverse_lazy('training-participant-list')

    def delete(self, request, *args, **kwargs):
        participant = self.get_object()
        response = super().delete(request, *args, **kwargs)
        log_activity(request.user, 'delete', f'Deleted Training Participant: {participant}')
        return response


class JobPostingListView(ListView):
    model = JobPosting
    template_name = 'human_resource/jobposting_list.html'

    def get_queryset(self):
        log_activity(self.request.user, 'view', 'Viewed Job Posting List')
        return super().get_queryset()

class JobPostingDetailView(DetailView):
    model = JobPosting
    template_name = 'human_resource/jobposting_detail.html'

    def get_object(self, queryset=None):
        job_posting = super().get_object(queryset)
        log_activity(self.request.user, 'view', f'Viewed Job Posting: {job_posting}')
        return job_posting

class JobPostingCreateView(CreateView):
    model = JobPosting
    template_name = 'human_resource/jobposting_form.html'
    fields = ['title', 'description', 'department', 'posting_date', 'closing_date']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'create', f'Created Job Posting: {self.object}')
        return response

class JobPostingUpdateView(UpdateView):
    model = JobPosting
    template_name = 'human_resource/jobposting_form.html'
    fields = ['title', 'description', 'department', 'posting_date', 'closing_date']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'update', f'Updated Job Posting: {self.object}')
        return response

class JobPostingDeleteView(DeleteView):
    model = JobPosting
    template_name = 'human_resource/jobposting_confirm_delete.html'
    success_url = reverse_lazy('job-posting-list')

    def delete(self, request, *args, **kwargs):
        job_posting = self.get_object()
        response = super().delete(request, *args, **kwargs)
        log_activity(request.user, 'delete', f'Deleted Job Posting: {job_posting}')
        return response


class ApplicantListView(ListView):
    model = Applicant
    template_name = 'human_resource/applicant_list.html'

    def get_queryset(self):
        log_activity(self.request.user, 'view', 'Viewed Applicant List')
        return super().get_queryset()

class ApplicantDetailView(DetailView):
    model = Applicant
    template_name = 'human_resource/applicant_detail.html'

    def get_object(self, queryset=None):
        applicant = super().get_object(queryset)
        log_activity(self.request.user, 'view', f'Viewed Applicant: {applicant}')
        return applicant

class ApplicantCreateView(CreateView):
    model = Applicant
    template_name = 'human_resource/applicant_form.html'
    fields = ['name', 'email', 'phone_number', 'resume', 'cover_letter', 'job_posting']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'create', f'Created Applicant: {self.object}')
        return response

class ApplicantUpdateView(UpdateView):
    model = Applicant
    template_name = 'human_resource/applicant_form.html'
    fields = ['name', 'email', 'phone_number', 'resume', 'cover_letter', 'job_posting']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'update', f'Updated Applicant: {self.object}')
        return response

class ApplicantDeleteView(DeleteView):
    model = Applicant
    template_name = 'applicants/applicant_confirm_delete.html'
    success_url = reverse_lazy('applicant-list')

    def delete(self, request, *args, **kwargs):
        applicant = self.get_object()
        response = super().delete(request, *args, **kwargs)
        log_activity(request.user, 'delete', f'Deleted Applicant: {applicant}')
        return response
