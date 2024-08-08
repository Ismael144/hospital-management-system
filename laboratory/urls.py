# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # LabTest URLs
    path('labtests/', views.LabTestListView.as_view(), name='labtest_list'),
    path('labtests/create/', views.LabTestCreateView.as_view(), name='labtest_create'),
    path('labtests/<int:pk>/', views.LabTestDetailView.as_view(), name='labtest_detail'),
    path('labtests/<int:pk>/update/', views.LabTestUpdateView.as_view(), name='labtest_update'),
    path('labtests/<int:pk>/delete/', views.LabTestDeleteView.as_view(), name='labtest_delete'),

    # Specimen URLs
    path('specimens/', views.SpecimenListView.as_view(), name='specimen_list'),
    path('specimens/create/', views.SpecimenCreateView.as_view(), name='specimen_create'),
    path('specimens/<int:pk>/', views.SpecimenDetailView.as_view(), name='specimen_detail'),
    path('specimens/<int:pk>/update/', views.SpecimenUpdateView.as_view(), name='specimen_update'),
    path('specimens/<int:pk>/delete/', views.SpecimenDeleteView.as_view(), name='specimen_delete'),

    # LabEquipment URLs
    path('equipment/', views.LabEquipmentListView.as_view(), name='equipment_list'),
    path('equipment/create/', views.LabEquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/', views.LabEquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/<int:pk>/update/', views.LabEquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', views.LabEquipmentDeleteView.as_view(), name='equipment_delete'),

    # LabResult URLs
    path('results/', views.LabResultListView.as_view(), name='result_list'),
    path('results/create/', views.LabResultCreateView.as_view(), name='result_create'),
    path('results/<int:pk>/', views.LabResultDetailView.as_view(), name='result_detail'),
    path('results/<int:pk>/update/', views.LabResultUpdateView.as_view(), name='result_update'),
    path('results/<int:pk>/delete/', views.LabResultDeleteView.as_view(), name='result_delete'),

    # LaboratoryInventory URLs
    path('inventory/', views.LaboratoryInventoryListView.as_view(), name='labinventory_list'),
    path('inventory/create/', views.LaboratoryInventoryCreateView.as_view(), name='labinventory_create'),
    path('inventory/<int:pk>/', views.LaboratoryInventoryDetailView.as_view(), name='labinventory_detail'),
    path('inventory/<int:pk>/update/', views.LaboratoryInventoryUpdateView.as_view(), name='labinventory_update'),
    path('inventory/<int:pk>/delete/', views.LaboratoryInventoryDeleteView.as_view(), name='labinventory_delete'),
]
