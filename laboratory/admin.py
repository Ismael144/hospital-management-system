from django.contrib import admin
from .models import LabTest, Specimen, LabEquipment, LabResult, LaboratoryInventory

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'test_code', 'patient', 'status', 'date_collected', 'date_reported')
    list_filter = ('status', 'date_collected')
    search_fields = ('test_name', 'test_code', 'patient__user__first_name', 'patient__user__last_name')
    readonly_fields = ('date_collected', 'date_reported')
    fieldsets = (
        (None, {
            'fields': ('patient', 'test_name', 'test_code', 'status', 'results')
        }),
        ('Dates', {
            'fields': ('date_collected', 'date_reported'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    list_display = ('lab_test', 'specimen_type', 'collection_date', 'condition')
    list_filter = ('condition', 'collection_date')
    search_fields = ('lab_test__test_name', 'specimen_type', 'notes')
    readonly_fields = ('collection_date',)

@admin.register(LabEquipment)
class LabEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'date_purchased', 'calibration_status')
    list_filter = ('calibration_status', 'date_purchased')
    search_fields = ('name', 'serial_number')
    readonly_fields = ('last_maintenance_date', 'next_maintenance_due')

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'test', 'result', 'date_performed', 'performed_by')
    list_filter = ('date_performed', 'performed_by')
    search_fields = ('appointment__id', 'test__test_name', 'result')
    readonly_fields = ('date_performed',)  # Ensures that this field cannot be edited in admin

@admin.register(LaboratoryInventory)
class LaboratoryInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'description', 'date_added', 'last_updated')
    list_filter = ('date_added',)
    search_fields = ('name', 'description')
    readonly_fields = ('date_added', 'last_updated')
