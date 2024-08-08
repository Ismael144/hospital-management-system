from django.urls import path
from .views import (ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView,
                    NoticeBoardListView, NoticeBoardDetailView, NoticeBoardCreateView, NoticeBoardUpdateView, NoticeBoardDeleteView,
                    StaffOnDutyListView, StaffOnDutyDetailView, StaffOnDutyCreateView, StaffOnDutyUpdateView, StaffOnDutyDeleteView, DepartmentListView, DepartmentCreateView, DepartmentDetailView, DepartmentUpdateView, DepartmentDeleteView)

from . import views 

urlpatterns = [
        # Department URLs
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='create_department'),
    path('departments/update/<int:pk>/', views.DepartmentUpdateView.as_view(), name='update_department'),
    path('departments/delete/<int:pk>/', views.DepartmentDeleteView.as_view(), name='delete_department'),

    # Shift URLs
    path('shifts/', views.ShiftListView.as_view(), name='shift_list'),
    path('shifts/create/', views.ShiftCreateView.as_view(), name='create_shift'),
    path('shifts/update/<int:pk>/', views.ShiftUpdateView.as_view(), name='update_shift'),
    path('shifts/delete/<int:pk>/', views.ShiftDeleteView.as_view(), name='delete_shift'),
    
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
