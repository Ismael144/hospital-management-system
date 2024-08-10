from django.urls import reverse_lazy
from django.views import generic
from .models import LabTest, Specimen, LabEquipment, LabResult, LaboratoryInventory
from .forms import LabTestForm, SpecimenForm, LabEquipmentForm, LabResultForm, LaboratoryInventoryForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from activities.models import Activity

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

# LabTest Views
@method_decorator([login_required, permission_required('app.view_labtest', raise_exception=True)], name='dispatch')
class LabTestListView(generic.ListView):
    model = LabTest
    template_name = 'laboratory/laboratory/labtest_list.html'
    context_object_name = 'labtests'

@method_decorator([login_required, permission_required('app.view_labtest', raise_exception=True)], name='dispatch')
class LabTestDetailView(generic.DetailView):
    model = LabTest
    template_name = 'laboratory/labtest_detail.html'
    context_object_name = 'labtest'

@method_decorator([login_required, permission_required('app.add_labtest', raise_exception=True)], name='dispatch')
class LabTestCreateView(generic.CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_url = reverse_lazy('labtest_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created lab test with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.change_labtest', raise_exception=True)], name='dispatch')
class LabTestUpdateView(generic.UpdateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_url = reverse_lazy('labtest_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated lab test with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.delete_labtest', raise_exception=True)], name='dispatch')
class LabTestDeleteView(generic.DeleteView):
    model = LabTest
    template_name = 'laboratory/labtest_confirm_delete.html'
    success_url = reverse_lazy('labtest_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted lab test with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Specimen Views
@method_decorator([login_required, permission_required('app.view_specimen', raise_exception=True)], name='dispatch')
class SpecimenListView(ListView):
    model = Specimen
    template_name = 'laboratory/specimen_list.html'
    context_object_name = 'specimens'

@method_decorator([login_required, permission_required('app.add_specimen', raise_exception=True)], name='dispatch')
class SpecimenCreateView(CreateView):
    model = Specimen
    template_name = 'laboratory/specimen_form.html'
    fields = ['lab_test', 'specimen_type', 'collection_date', 'condition', 'notes']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created specimen with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.view_specimen', raise_exception=True)], name='dispatch')
class SpecimenDetailView(DetailView):
    model = Specimen
    template_name = 'laboratory/specimen_detail.html'
    context_object_name = 'specimen'

@method_decorator([login_required, permission_required('app.change_specimen', raise_exception=True)], name='dispatch')
class SpecimenUpdateView(UpdateView):
    model = Specimen
    template_name = 'laboratory/specimen_form.html'
    fields = ['lab_test', 'specimen_type', 'collection_date', 'condition', 'notes']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated specimen with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.delete_specimen', raise_exception=True)], name='dispatch')
class SpecimenDeleteView(DeleteView):
    model = Specimen
    template_name = 'laboratory/specimen_confirm_delete.html'
    success_url = '/specimens/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted specimen with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# LabEquipment Views
@method_decorator([login_required, permission_required('app.view_labequipment', raise_exception=True)], name='dispatch')
class LabEquipmentListView(generic.ListView):
    model = LabEquipment
    template_name = 'laboratory/labequipment_list.html'
    context_object_name = 'labequipments'

@method_decorator([login_required, permission_required('app.view_labequipment', raise_exception=True)], name='dispatch')
class LabEquipmentDetailView(generic.DetailView):
    model = LabEquipment
    template_name = 'laboratory/labequipment_detail.html'
    context_object_name = 'labequipment'

@method_decorator([login_required, permission_required('app.add_labequipment', raise_exception=True)], name='dispatch')
class LabEquipmentCreateView(generic.CreateView):
    model = LabEquipment
    form_class = LabEquipmentForm
    template_name = 'laboratory/labequipment_form.html'
    success_url = reverse_lazy('labequipment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created lab equipment with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.change_labequipment', raise_exception=True)], name='dispatch')
class LabEquipmentUpdateView(generic.UpdateView):
    model = LabEquipment
    form_class = LabEquipmentForm
    template_name = 'laboratory/labequipment_form.html'
    success_url = reverse_lazy('labequipment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated lab equipment with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.delete_labequipment', raise_exception=True)], name='dispatch')
class LabEquipmentDeleteView(generic.DeleteView):
    model = LabEquipment
    template_name = 'laboratory/labequipment_confirm_delete.html'
    success_url = reverse_lazy('labequipment_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted lab equipment with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# LabResult Views
@method_decorator([login_required, permission_required('app.view_labresult', raise_exception=True)], name='dispatch')
class LabResultListView(ListView):
    model = LabResult
    template_name = 'laboratory/labresult_list.html'
    context_object_name = 'labresults'

@method_decorator([login_required, permission_required('app.add_labresult', raise_exception=True)], name='dispatch')
class LabResultCreateView(CreateView):
    model = LabResult
    template_name = 'laboratory/labresult_form.html'
    fields = ['appointment', 'test', 'result', 'performed_by']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created lab result with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.view_labresult', raise_exception=True)], name='dispatch')
class LabResultDetailView(DetailView):
    model = LabResult
    template_name = 'laboratory/labresult_detail.html'
    context_object_name = 'labresult'

@method_decorator([login_required, permission_required('app.change_labresult', raise_exception=True)], name='dispatch')
class LabResultUpdateView(UpdateView):
    model = LabResult
    template_name = 'laboratory/labresult_form.html'
    fields = ['appointment', 'test', 'result', 'date_performed', 'performed_by']

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated lab result with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.delete_labresult', raise_exception=True)], name='dispatch')
class LabResultDeleteView(DeleteView):
    model = LabResult
    template_name = 'laboratory/labresult_confirm_delete.html'
    success_url = '/results/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted lab result with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# LaboratoryInventory Views
@method_decorator([login_required, permission_required('app.view_laboratoryinventory', raise_exception=True)], name='dispatch')
class LaboratoryInventoryListView(generic.ListView):
    model = LaboratoryInventory
    template_name = 'laboratory/laboratoryinventory_list.html'
    context_object_name = 'laboratoryinventory'

@method_decorator([login_required, permission_required('app.view_laboratoryinventory', raise_exception=True)], name='dispatch')
class LaboratoryInventoryDetailView(generic.DetailView):
    model = LaboratoryInventory
    template_name = 'laboratory/laboratoryinventory_detail.html'
    context_object_name = 'laboratoryinventory'

@method_decorator([login_required, permission_required('app.add_laboratoryinventory', raise_exception=True)], name='dispatch')
class LaboratoryInventoryCreateView(generic.CreateView):
    model = LaboratoryInventory
    form_class = LaboratoryInventoryForm
    template_name = 'laboratory/laboratoryinventory_form.html'
    success_url = reverse_lazy('laboratoryinventory_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created laboratory inventory with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.change_laboratoryinventory', raise_exception=True)], name='dispatch')
class LaboratoryInventoryUpdateView(generic.UpdateView):
    model = LaboratoryInventory
    form_class = LaboratoryInventoryForm
    template_name = 'laboratory/laboratoryinventory_form.html'
    success_url = reverse_lazy('laboratoryinventory_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated laboratory inventory with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.delete_laboratoryinventory', raise_exception=True)], name='dispatch')
class LaboratoryInventoryDeleteView(generic.DeleteView):
    model = LaboratoryInventory
    template_name = 'laboratory/laboratoryinventory_confirm_delete.html'
    success_url = reverse_lazy('laboratoryinventory_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted laboratory inventory with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)
