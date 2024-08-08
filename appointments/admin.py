from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'nurse', 'appointment_date', 'status')
    list_filter = ('status', 'doctor', 'nurse', 'appointment_date')
    search_fields = ('patient__user__email', 'doctor__user__email', 'nurse__user__email')
    ordering = ('-appointment_date',)

    def patient(self, obj):
        return obj.patient.user.email

    def doctor(self, obj):
        return obj.doctor.user.email if obj.doctor else 'N/A'

    def nurse(self, obj):
        return obj.nurse.user.email if obj.nurse else 'N/A'

    patient.admin_order_field = 'patient__user__email'
    doctor.admin_order_field = 'doctor__user__email'
    nurse.admin_order_field = 'nurse__user__email'
