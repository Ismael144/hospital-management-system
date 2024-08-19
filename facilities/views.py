from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Room, Sickbay, Allocation, Inventory, Supplier
from activities.models import Activity
from .forms import InventoryForm, InventoryForm, SupplierForm
from mixins import ListViewMixin, DetailViewMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .forms import RoomForm

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

# Decorators for class-based views
def permission_required_view(permission):
    return method_decorator(permission_required(permission, raise_exception=True))

def login_required_view():
    return method_decorator(login_required)

# Room views
@method_decorator([login_required, permission_required('facilities.view_room', raise_exception=True)], name='dispatch')
class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

@method_decorator([login_required, permission_required('facilities.view_room', raise_exception=True)], name='dispatch')
class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'

@method_decorator([login_required, permission_required('facilities.add_room', raise_exception=True)], name='dispatch')
class RoomCreateView(CreateView):
    model = Room
    template_name = 'room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new room with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.change_room', raise_exception=True)], name='dispatch')
class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('room_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated room with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.delete_room', raise_exception=True)], name='dispatch')
class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted room with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Sickbay views
@method_decorator([login_required, permission_required('facilities.view_sickbay', raise_exception=True)], name='dispatch')
class SickbayListView(ListView):
    model = Sickbay
    template_name = 'sickbay_list.html'
    context_object_name = 'sickbays'

@method_decorator([login_required, permission_required('facilities.view_sickbay', raise_exception=True)], name='dispatch')
class SickbayDetailView(DetailView):
    model = Sickbay
    template_name = 'sickbay_detail.html'

@method_decorator([login_required, permission_required('facilities.add_sickbay', raise_exception=True)], name='dispatch')
class SickbayCreateView(CreateView):
    model = Sickbay
    template_name = 'sickbay_form.html'
    fields = ['sickbay_number', 'status', 'capacity', 'description']
    success_url = reverse_lazy('sickbay_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new sickbay with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.change_sickbay', raise_exception=True)], name='dispatch')
class SickbayUpdateView(UpdateView):
    model = Sickbay
    template_name = 'sickbay_form.html'
    fields = ['sickbay_number', 'status', 'capacity', 'description']
    success_url = reverse_lazy('sickbay_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated sickbay with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.delete_sickbay', raise_exception=True)], name='dispatch')
class SickbayDeleteView(DeleteView):
    model = Sickbay
    template_name = 'sickbay_confirm_delete.html'
    success_url = reverse_lazy('sickbay_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted sickbay with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Allocation views
@method_decorator([login_required, permission_required('facilities.view_allocation', raise_exception=True)], name='dispatch')
class AllocationListView(ListView):
    model = Allocation
    template_name = 'allocation_list.html'
    context_object_name = 'allocations'

@method_decorator([login_required, permission_required('facilities.view_allocation', raise_exception=True)], name='dispatch')
class AllocationDetailView(DetailView):
    model = Allocation
    template_name = 'allocation_detail.html'
    context_object_name = 'allocation'

@method_decorator([login_required, permission_required('facilities.add_allocation', raise_exception=True)], name='dispatch')
class AllocationCreateView(CreateView):
    model = Allocation
    template_name = 'allocation_form.html'
    fields = ['patient', 'allocation_type', 'room', 'sickbay']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new allocation with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.change_allocation', raise_exception=True)], name='dispatch')
class AllocationUpdateView(UpdateView):
    model = Allocation
    template_name = 'allocation_form.html'
    fields = ['patient', 'allocation_type', 'room', 'sickbay']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated allocation with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.delete_allocation', raise_exception=True)], name='dispatch')
class AllocationDeleteView(DeleteView):
    model = Allocation
    template_name = 'allocation_confirm_delete.html'
    success_url = reverse_lazy('allocation_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted allocation with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Inventory views
@method_decorator([login_required, permission_required('facilities.view_inventory', raise_exception=True)], name='dispatch')
class InventoryListView(ListViewMixin, ListView):
    model = Inventory
    template_name = 'inventory_list.html'
    context_object_name = 'inventories'

@method_decorator([login_required, permission_required('facilities.view_inventory', raise_exception=True)], name='dispatch')
class InventoryDetailView(DetailViewMixin, DetailView):
    model = Inventory
    template_name = 'inventory_detail.html'
    context_object_name = 'inventory'

@method_decorator([login_required, permission_required('facilities.add_inventory', raise_exception=True)], name='dispatch')
class InventoryCreateView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'facilities/inventory_form.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new inventory item with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.change_inventory', raise_exception=True)], name='dispatch')
class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'facilities/inventory_form.html'
    success_url = reverse_lazy('inventory_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated inventory item with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('facilities.delete_inventory', raise_exception=True)], name='dispatch')
class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted inventory item with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

class SupplierListView(ListView):
    model = Supplier
    template_name = 'facilities/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'facilities/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'facilities/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'facilities/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'facilities/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')