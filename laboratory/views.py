# views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import LabTest, Specimen, LabEquipment, LabResult, LaboratoryInventory
from .forms import LabTestForm, SpecimenForm, LabEquipmentForm, LabResultForm, LaboratoryInventoryForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# LabTest Views
class LabTestListView(generic.ListView):
    model = LabTest
    template_name = 'laboratory/laboratory/labtest_list.html'
    context_object_name = 'labtests'

class LabTestDetailView(generic.DetailView):
    model = LabTest
    template_name = 'laboratory/labtest_detail.html'
    context_object_name = 'labtest'

class LabTestCreateView(generic.CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_url = reverse_lazy('labtest_list')

class LabTestUpdateView(generic.UpdateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_url = reverse_lazy('labtest_list')

class LabTestDeleteView(generic.DeleteView):
    model = LabTest
    template_name = 'laboratory/labtest_confirm_delete.html'
    success_url = reverse_lazy('labtest_list')

# Specimen Views

class SpecimenListView(ListView):
    model = Specimen
    template_name = 'laboratory/specimen_list.html'
    context_object_name = 'specimens'

class SpecimenCreateView(CreateView):
    model = Specimen
    template_name = 'laboratory/specimen_form.html'
    fields = ['lab_test', 'specimen_type', 'collection_date', 'condition', 'notes']

class SpecimenDetailView(DetailView):
    model = Specimen
    template_name = 'laboratory/specimen_detail.html'
    context_object_name = 'specimen'

class SpecimenUpdateView(UpdateView):
    model = Specimen
    template_name = 'laboratory/specimen_form.html'
    fields = ['lab_test', 'specimen_type', 'collection_date', 'condition', 'notes']

class SpecimenDeleteView(DeleteView):
    model = Specimen
    template_name = 'laboratory/specimen_confirm_delete.html'
    success_url = '/specimens/'


# LabEquipment Views
class LabEquipmentListView(generic.ListView):
    model = LabEquipment
    template_name = 'laboratory/labequipment_list.html'
    context_object_name = 'labequipments'

class LabEquipmentDetailView(generic.DetailView):
    model = LabEquipment
    template_name = 'laboratory/labequipment_detail.html'
    context_object_name = 'labequipment'

class LabEquipmentCreateView(generic.CreateView):
    model = LabEquipment
    form_class = LabEquipmentForm
    template_name = 'laboratory/labequipment_form.html'
    success_url = reverse_lazy('labequipment_list')

class LabEquipmentUpdateView(generic.UpdateView):
    model = LabEquipment
    form_class = LabEquipmentForm
    template_name = 'laboratory/labequipment_form.html'
    success_url = reverse_lazy('labequipment_list')

class LabEquipmentDeleteView(generic.DeleteView):
    model = LabEquipment
    template_name = 'laboratory/labequipment_confirm_delete.html'
    success_url = reverse_lazy('labequipment_list')

# LabResult Views

class LabResultListView(ListView):
    model = LabResult
    template_name = 'laboratory/labresult_list.html'
    context_object_name = 'labresults'

class LabResultCreateView(CreateView):
    model = LabResult
    template_name = 'laboratory/labresult_form.html'
    fields = ['appointment', 'test', 'result', 'performed_by']

class LabResultDetailView(DetailView):
    model = LabResult
    template_name = 'laboratory/labresult_detail.html'
    context_object_name = 'labresult'

class LabResultUpdateView(UpdateView):
    model = LabResult
    template_name = 'laboratory/labresult_form.html'
    fields = ['appointment', 'test', 'result', 'date_performed', 'performed_by']

class LabResultDeleteView(DeleteView):
    model = LabResult
    template_name = 'laboratory/labresult_confirm_delete.html'
    success_url = '/results/'

# LaboratoryInventory Views
class LaboratoryInventoryListView(generic.ListView):
    model = LaboratoryInventory
    template_name = 'laboratory/laboratoryinventory_list.html'
    context_object_name = 'inventory_items'

class LaboratoryInventoryDetailView(generic.DetailView):
    model = LaboratoryInventory
    template_name = 'laboratory/laboratoryinventory_detail.html'
    context_object_name = 'inventory_item'

class LaboratoryInventoryCreateView(generic.CreateView):
    model = LaboratoryInventory
    form_class = LaboratoryInventoryForm
    template_name = 'laboratory/laboratoryinventory_form.html'
    success_url = reverse_lazy('labinventory_list')

class LaboratoryInventoryUpdateView(generic.UpdateView):
    model = LaboratoryInventory
    form_class = LaboratoryInventoryForm
    template_name = 'laboratory/laboratoryinventory_form.html'
    success_url = reverse_lazy('labinventory_list')

class LaboratoryInventoryDeleteView(generic.DeleteView):
    model = LaboratoryInventory
    template_name = 'laboratory/laboratoryinventory_confirm_delete.html'
    success_url = reverse_lazy('labinventory_list')
