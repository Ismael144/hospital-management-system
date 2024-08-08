from django.urls import path 
from .views import *

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    path('pharmacists/', PharmacistListView.as_view(), name='pharmacist-list'),
    path('pharmacists/<int:pk>/', PharmacistDetailView.as_view(), name='pharmacist-detail'),
    path('pharmacists/create/', PharmacistCreateView.as_view(), name='pharmacist-create'),
    path('pharmacists/<int:pk>/edit/', PharmacistUpdateView.as_view(), name='pharmacist-update'),
    path('pharmacists/<int:pk>/delete/', PharmacistDeleteView.as_view(), name='pharmacist-delete'),

    path('patients/discharge-summaries/', DischargeSummaryListView.as_view(), name='discharge_summary_list'),
    path('patients/discharge-summary/create/', DischargeSummaryCreateView.as_view(), name='discharge_summary_create'),
    path('patients/discharge-summary/<int:pk>/update/', DischargeSummaryUpdateView.as_view(), name='discharge_summary_update'),
    path('patients/discharge-summary/<int:pk>/', DischargeSummaryDetailView.as_view(), name='discharge_summary_detail'),
    path('patients/discharge-summary/<int:pk>/delete/', DischargeSummaryDeleteView.as_view(), name='discharge_summary_delete'),
    
    # Receptionist URLs
    path('receptionists/', ReceptionistListView.as_view(), name='receptionist_list'),
    path('receptionists/<int:pk>/', ReceptionistDetailView.as_view(), name='receptionist_detail'),
    path('receptionists/create/', ReceptionistCreateView.as_view(), name='receptionist_create'),
    path('receptionists/<int:pk>/update/', ReceptionistUpdateView.as_view(), name='receptionist_update'),
    path('receptionists/<int:pk>/delete/', ReceptionistDeleteView.as_view(), name='receptionist_delete'),

    # Patient URLs
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/create/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/update/', PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),

    # Doctor URLs
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor_delete'),

    # Nurse URLs
    path('nurses/', NurseListView.as_view(), name='nurse_list'),
    path('nurses/<int:pk>/', NurseDetailView.as_view(), name='nurse_detail'),
    path('nurses/create/', NurseCreateView.as_view(), name='nurse_create'),
    path('nurses/<int:pk>/update/', NurseUpdateView.as_view(), name='nurse_update'),
    path('nurses/<int:pk>/delete/', NurseDeleteView.as_view(), name='nurse_delete'),

    # Lab Technician URLs 
    path('lab_technicians/', LabTechnicianListView.as_view(), name='lab_technician_list'),
    path('lab_technicians/create/', LabTechnicianCreateView.as_view(), name='lab_technician_create'),
    path('lab_technicians/update/<int:pk>/', LabTechnicianUpdateView.as_view(), name='lab_technician_update'),
    path('lab_technicians/delete/<int:pk>/', LabTechnicianDeleteView.as_view(), name='lab_technician_delete'),
    path('lab-technician/<int:pk>/', LabTechnicianDetailView.as_view(), name='lab_technician_detail'),

    # Case Manager URLs
    path('case_managers/', CaseManagerListView.as_view(), name='case_manager_list'),
    path('case_managers/create/', CaseManagerCreateView.as_view(), name='case_manager_create'),
    path('case_managers/<int:pk>/', CaseManagerDetailView.as_view(), name='case_manager_detail'),
    path('case_managers/<int:pk>/update/', CaseManagerUpdateView.as_view(), name='case_manager_update'),

    # Accountant URLs
    path('accountants/', AccountantListView.as_view(), name='accountant_list'),
    path('accountants/create/', AccountantCreateView.as_view(), name='accountant_create'),
    path('accountants/<int:pk>/update/', AccountantUpdateView.as_view(), name='accountant_update'),
    path('accountants/<int:pk>/', AccountantDetailView.as_view(), name='accountant_detail'),
    path('accountants/<int:pk>/delete/', AccountantDeleteView.as_view(), name='accountant_delete'),
]
