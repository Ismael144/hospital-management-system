from django.urls import path
from .views import (
    LeaveListView, LeaveDetailView, LeaveCreateView,
    LeaveUpdateView, LeaveDeleteView,
    PerformanceReviewListView, PerformanceReviewDetailView,
    PerformanceReviewCreateView, PerformanceReviewUpdateView,
    PerformanceReviewDeleteView,
    TrainingListView, TrainingDetailView, TrainingCreateView,
    TrainingUpdateView, TrainingDeleteView,
    TrainingParticipantListView, TrainingParticipantDetailView,
    TrainingParticipantCreateView, TrainingParticipantUpdateView,
    TrainingParticipantDeleteView,
    JobPostingListView, JobPostingDetailView, JobPostingCreateView,
    JobPostingUpdateView, JobPostingDeleteView,
    ApplicantListView, ApplicantDetailView, ApplicantCreateView,
    ApplicantUpdateView, ApplicantDeleteView
)
from .views import *

urlpatterns = [
    # Leave URLs
    path('leaves/', LeaveListView.as_view(), name='leave-list'),
    path('leaves/<int:pk>/', LeaveDetailView.as_view(), name='leave-detail'),
    path('leaves/create/', LeaveCreateView.as_view(), name='leave-create'),
    path('leaves/<int:pk>/edit/', LeaveUpdateView.as_view(), name='leave-update'),
    path('leaves/<int:pk>/delete/', LeaveDeleteView.as_view(), name='leave-delete'),

    # PerformanceReview URLs
    path('performance-reviews/', PerformanceReviewListView.as_view(), name='performance-review-list'),
    path('performance-reviews/<int:pk>/', PerformanceReviewDetailView.as_view(), name='performance-review-detail'),
    path('performance-reviews/create/', PerformanceReviewCreateView.as_view(), name='performance-review-create'),
    path('performance-reviews/<int:pk>/edit/', PerformanceReviewUpdateView.as_view(), name='performance-review-update'),
    path('performance-reviews/<int:pk>/delete/', PerformanceReviewDeleteView.as_view(), name='performance-review-delete'),

    # Training URLs
    path('trainings/', TrainingListView.as_view(), name='training-list'),
    path('trainings/<int:pk>/', TrainingDetailView.as_view(), name='training-detail'),
    path('trainings/create/', TrainingCreateView.as_view(), name='training-create'),
    path('trainings/<int:pk>/edit/', TrainingUpdateView.as_view(), name='training-update'),
    path('trainings/<int:pk>/delete/', TrainingDeleteView.as_view(), name='training-delete'),

    # TrainingParticipant URLs
    path('training-participants/', TrainingParticipantListView.as_view(), name='training-participant-list'),
    path('training-participants/<int:pk>/', TrainingParticipantDetailView.as_view(), name='training-participant-detail'),
    path('training-participants/create/', TrainingParticipantCreateView.as_view(), name='training-participant-create'),
    path('training-participants/<int:pk>/edit/', TrainingParticipantUpdateView.as_view(), name='training-participant-update'),
    path('training-participants/<int:pk>/delete/', TrainingParticipantDeleteView.as_view(), name='training-participant-delete'),

    # JobPosting URLs
    path('job-postings/', JobPostingListView.as_view(), name='job-posting-list'),
    path('job-postings/<int:pk>/', JobPostingDetailView.as_view(), name='job-posting-detail'),
    path('job-postings/create/', JobPostingCreateView.as_view(), name='job-posting-create'),
    path('job-postings/<int:pk>/edit/', JobPostingUpdateView.as_view(), name='job-posting-update'),
    path('job-postings/<int:pk>/delete/', JobPostingDeleteView.as_view(), name='job-posting-delete'),

    # Applicant URLs
    path('applicants/', ApplicantListView.as_view(), name='applicant-list'),
    path('applicants/<int:pk>/', ApplicantDetailView.as_view(), name='applicant-detail'),
    path('applicants/create/', ApplicantCreateView.as_view(), name='applicant-create'),
    path('applicants/<int:pk>/edit/', ApplicantUpdateView.as_view(), name='applicant-update'),
    path('applicants/<int:pk>/delete/', ApplicantDeleteView.as_view(), name='applicant-delete'),

    # Department URLs
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', DepartmentCreateView.as_view(), name='create_department'),
    path('departments/update/<int:pk>/', DepartmentUpdateView.as_view(), name='update_department'),
    path('departments/delete/<int:pk>/', DepartmentDeleteView.as_view(), name='delete_department'),

    # Shift URLs
    path('shifts/', ShiftListView.as_view(), name='shift_list'),
    path('shifts/create/', ShiftCreateView.as_view(), name='create_shift'),
    path('shifts/update/<int:pk>/', ShiftUpdateView.as_view(), name='update_shift'),
    path('shifts/delete/<int:pk>/', ShiftDeleteView.as_view(), name='delete_shift'),
    
    path('schedules/', ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedules/add/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>/edit/', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule_delete'),

    path('noticeboard/', NoticeBoardListView.as_view(), name='noticeboard_list'),
    path('noticeboard/<int:pk>/', NoticeBoardDetailView.as_view(), name='noticeboard_detail'),
    path('noticeboard/add/', NoticeBoardCreateView.as_view(), name='noticeboard_create'),
    path('noticeboard/<int:pk>/edit/', NoticeBoardUpdateView.as_view(), name='noticeboard_update'),
    path('noticeboard/<int:pk>/delete/', NoticeBoardDeleteView.as_view(), name='noticeboard_delete'),

    path('staffonduty/', StaffOnDutyListView.as_view(), name='staffonduty_list'),
    path('staffonduty/<int:pk>/', StaffOnDutyDetailView.as_view(), name='staffonduty_detail'),
    path('staffonduty/add/', StaffOnDutyCreateView.as_view(), name='staffonduty_create'),
    path('staffonduty/<int:pk>/edit/', StaffOnDutyUpdateView.as_view(), name='staffonduty_update'),
    path('staffonduty/<int:pk>/delete/', StaffOnDutyDeleteView.as_view(), name='staffonduty_delete'),
    
    # Department URLs
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/new/', DepartmentCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/edit/', DepartmentUpdateView.as_view(), name='department-update'),
    path('departments/<int:pk>/delete/', DepartmentDeleteView.as_view(), name='department-delete'),
]
