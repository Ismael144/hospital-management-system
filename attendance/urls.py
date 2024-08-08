from django.urls import path
from .views import AttendanceListView, AttendanceDetailView, AttendanceCreateView, AttendanceUpdateView, search_attendance

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance_list'),
    path('<int:pk>/', AttendanceDetailView.as_view(), name='attendance_detail'),
    path('create/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('search/', search_attendance, name='search_attendance'),
    path('<int:pk>/update/', AttendanceUpdateView.as_view(), name='attendance_update'),
]

