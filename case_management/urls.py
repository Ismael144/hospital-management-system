from django.urls import path
from .views import (
    CaseListView, CaseDetailView, CaseCreateView, CaseUpdateView, CaseDeleteView,
    CaseNoteCreateView, CarePlanCreateView, CarePlanDetailView
)

urlpatterns = [
    path('cases/', CaseListView.as_view(), name='case_list'),
    path('cases/<int:pk>/', CaseDetailView.as_view(), name='case_detail'),
    path('cases/create/', CaseCreateView.as_view(), name='case_create'),
    path('cases/<int:pk>/update/', CaseUpdateView.as_view(), name='case_update'),
    path('cases/<int:pk>/delete/', CaseDeleteView.as_view(), name='case_delete'),
    
    path('cases/<int:pk>/note/create/', CaseNoteCreateView.as_view(), name='case_note_create'),
    
    path('care-plans/create/', CarePlanCreateView.as_view(), name='care_plan_create'),
    path('care-plans/<int:pk>/', CarePlanDetailView.as_view(), name='care_plan_detail'),
]
