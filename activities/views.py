from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from .models import Activity

class ActivityLogListView(ListView):
    model = Activity
    template_name = 'activity_log_list.html'
    context_object_name = 'activity_logs'
    ordering = ['-timestamp']  # Order logs by most recent first

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role.lower() == 'admin' or self.request.user.role.lower() == '': 
            return queryset
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset