from django.urls import path 
from .views import *

urlpatterns = [
    path('', ActivityLogListView.as_view(), name='activity_log_list')
]
