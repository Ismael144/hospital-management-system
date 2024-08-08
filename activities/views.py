from django.views.generic import ListView
from .models import Activity

class ActivityLogListView(ListView):
    model = Activity
    template_name = 'activity_log_list.html'
    context_object_name = 'activity_logs'
    ordering = ['-timestamp']  # Order logs by most recent first
