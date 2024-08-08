from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Case, CaseNote, CarePlan
from .forms import CaseForm, CaseNoteForm, CarePlanForm

class CaseListView(ListView):
    model = Case
    template_name = 'cases/case_list.html'
    context_object_name = 'cases'

class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'

class CaseUpdateView(UpdateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'

class CaseDeleteView(DeleteView):
    model = Case
    success_url = reverse_lazy('case_list')
    template_name = 'case_confirm_delete.html'

class CaseNoteCreateView(CreateView):
    model = CaseNote
    form_class = CaseNoteForm
    template_name = 'cases/case_note_form.html'

class CarePlanCreateView(CreateView):
    model = CarePlan
    form_class = CarePlanForm
    template_name = 'cases/care_plan_form.html'

class CarePlanDetailView(DetailView):
    model = CarePlan
    template_name = 'care_plan_detail.html'
    context_object_name = 'care_plan'
