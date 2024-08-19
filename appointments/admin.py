from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'employee',  'appointment_date', 'status')
    list_filter = ('status', 'employee', 'appointment_date')
    search_fields = ('patient__user__email', 'employee__user__email')
    ordering = ('-appointment_date',)

    def patient(self, obj):
        return obj.patient.user.email

    def employee(self, obj):
        return obj.employee.user.email if obj.employee else 'N/A'
    
    patient.admin_order_field = 'patient__user__email'
    employee.admin_order_field = 'employee__user__email'
