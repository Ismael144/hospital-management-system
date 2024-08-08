from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Room, Sickbay, Allocation, Inventory
from activities.models import Activity
from .forms import InventoryCreateForm, InventoryUpdateForm
from mixins import ListViewMixin, DetailViewMixin

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

# Room views
class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'

class RoomCreateView(CreateView):
    model = Room
    template_name = 'room_form.html'
    fields = ['room_number', 'status', 'room_type', 'capacity']
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new room with ID {self.object.pk}')
        return response

class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'room_form.html'
    fields = ['room_number', 'status', 'room_type', 'capacity']
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated room with ID {self.object.pk}')
        return response

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted room with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Sickbay views
class SickbayListView(ListView):
    model = Sickbay
    template_name = 'sickbay_list.html'
    context_object_name = 'sickbays'

class SickbayDetailView(DetailView):
    model = Sickbay
    template_name = 'sickbay_detail.html'

class SickbayCreateView(CreateView):
    model = Sickbay
    template_name = 'sickbay_form.html'
    fields = ['sickbay_number', 'status', 'capacity', 'description']
    success_url = reverse_lazy('sickbay_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new sickbay with ID {self.object.pk}')
        return response

class SickbayUpdateView(UpdateView):
    model = Sickbay
    template_name = 'sickbay_form.html'
    fields = ['sickbay_number', 'status', 'capacity', 'description']
    success_url = reverse_lazy('sickbay_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated sickbay with ID {self.object.pk}')
        return response

class SickbayDeleteView(DeleteView):
    model = Sickbay
    template_name = 'sickbay_confirm_delete.html'
    success_url = reverse_lazy('sickbay_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted sickbay with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Allocation views
class AllocationListView(ListView):
    model = Allocation
    template_name = 'allocation_list.html'
    context_object_name = 'allocations'

class AllocationDetailView(DetailView):
    model = Allocation
    template_name = 'allocation_detail.html'
    context_object_name = 'allocation'

class AllocationCreateView(CreateView):
    model = Allocation
    template_name = 'allocation_form.html'
    fields = ['patient', 'allocation_type', 'room', 'sickbay']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new allocation with ID {self.object.pk}')
        return response

class AllocationUpdateView(UpdateView):
    model = Allocation
    template_name = 'allocation_form.html'
    fields = ['patient', 'allocation_type', 'room', 'sickbay']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated allocation with ID {self.object.pk}')
        return response

class AllocationDeleteView(DeleteView):
    model = Allocation
    template_name = 'allocation_confirm_delete.html'
    success_url = reverse_lazy('allocation_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted allocation with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Inventory views
class InventoryListView(ListViewMixin, ListView):
    model = Inventory
    template_name = 'inventory_list.html'
    context_object_name = 'inventories'

class InventoryDetailView(DetailViewMixin, DetailView):
    model = Inventory
    template_name = 'inventory_detail.html'
    context_object_name = 'inventory'

class InventoryCreateView(CreateView):
    model = Inventory
    form_class = InventoryCreateForm
    template_name = 'inventory_create.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new inventory item with ID {self.object.pk}')
        return response

class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryUpdateForm
    template_name = 'inventory_update.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated inventory item with ID {self.object.pk}')
        return response

class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted inventory item with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)
