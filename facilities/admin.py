from django.contrib import admin
from .models import Room, Sickbay, Allocation, Inventory

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'status', 'room_type', 'capacity')

@admin.register(Sickbay)
class SickbayAdmin(admin.ModelAdmin):
    list_display = ('sickbay_number', 'status', 'capacity', 'description')

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allocation_type', 'room', 'sickbay', 'date_allocated')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'date_added', 'last_updated')