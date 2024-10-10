from django.urls import path
from .views import *

urlpatterns = [
    path('medications/', MedicationListView.as_view(), name='medication_list'),
    path('medications/<int:pk>/', MedicationDetailView.as_view(), name='medication_detail'),
    path('medications/new/', MedicationCreateView.as_view(), name='medication_create'),
    path('medications/<int:pk>/edit/', MedicationUpdateView.as_view(), name='medication_update'),
    path('medications/<int:pk>/delete/', MedicationDeleteView.as_view(), name='medication_delete'),
    
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/<int:pk>/', PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('prescriptions/new/', PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/<int:pk>/edit/', PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription_delete'),
    
    path('dispensations/', DispensationListView.as_view(), name='dispensation_list'),
    path('dispensations/<int:pk>/', DispensationDetailView.as_view(), name='dispensation_detail'),
    path('dispensations/new/', DispensationCreateView.as_view(), name='dispensation_create'),
    path('dispensations/<int:pk>/edit/', DispensationUpdateView.as_view(), name='dispensation_update'),
    path('dispensations/<int:pk>/delete/', DispensationDeleteView.as_view(), name='dispensation_delete'),

        path('medication-assignments/', MedicationAssignmentListView.as_view(), name='medication-assignment-list'),
    path('medication-assignments/<int:pk>/', MedicationAssignmentDetailView.as_view(), name='medication-assignment-detail'),
    path('medication-assignments/create/', MedicationAssignmentCreateView.as_view(), name='medication-assignment-create'),
    path('medication-assignments/<int:pk>/update/', MedicationAssignmentUpdateView.as_view(), name='medication-assignment-update'),
    path('medication-assignments/<int:pk>/delete/', MedicationAssignmentDeleteView.as_view(), name='medication-assignment-delete'),
]
