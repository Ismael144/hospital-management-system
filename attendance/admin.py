from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'date', 'time_in', 'time_out', 'status')
    list_filter = ('role', 'status', 'date')
    search_fields = ('user__username', 'user__email', 'date')
    date_hierarchy = 'date'
    ordering = ('-date', 'time_in')

admin.site.register(Attendance, AttendanceAdmin)
