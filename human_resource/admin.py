from django.contrib import admin
from .models import Leave, PerformanceReview, Training, TrainingParticipant, JobPosting, Applicant

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'leave_type')
    list_filter = ('leave_type', 'status', 'approved_by')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_date', 'performance_score')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'reviewer__user__first_name', 'reviewer__user__last_name')
    list_filter = ('reviewer',)
    date_hierarchy = 'review_date'
    ordering = ('-review_date',)

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'trainer')
    search_fields = ('title', 'description', 'trainer')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

@admin.register(TrainingParticipant)
class TrainingParticipantAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training', 'completion_date', 'certificate_issued')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'training__title')
    list_filter = ('certificate_issued', 'training')
    date_hierarchy = 'completion_date'
    ordering = ('-completion_date',)

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'posting_date', 'closing_date', 'status')
    search_fields = ('title', 'department__name', 'description')
    list_filter = ('status', 'department')
    date_hierarchy = 'posting_date'
    ordering = ('-posting_date',)

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_posting', 'email', 'application_date', 'status')
    search_fields = ('name', 'email', 'job_posting__title')
    list_filter = ('status', 'job_posting')
    date_hierarchy = 'application_date'
    ordering = ('-application_date',)
