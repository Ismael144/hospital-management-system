from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Case, CaseNote, CarePlan
from .forms import CaseForm, CaseNoteForm, CarePlanForm
from activities.models import Activity
from django.http import HttpResponseForbidden
from accounts.models import Employee, CaseManager
from django.shortcuts import redirect

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

@method_decorator([login_required, permission_required('app.view_case', raise_exception=True)], name='dispatch')
class CaseListView(ListView):
    model = Case
    template_name = 'cases/case_list.html'
    context_object_name = 'cases'

@method_decorator([login_required, permission_required('app.view_case', raise_exception=True)], name='dispatch')
class CaseDetailView(DetailView):
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

class CaseCreateView(CreateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'
    success_url = reverse_lazy('case_list')  # Define the success URL after creation

    def form_valid(self, form):
        # Automatically set the case_manager to the logged-in user if they are a case manager
        if self.request.user.role == 'case_manager':
            case = form.save(commit=False)
            employee = Employee.objects.filter(user=self.request.user).first()
            case_manager = CaseManager.objects.filter(employee=employee).first()
            case.case_manager = case_manager  # Assign the current user as case_manager
            case.save()

            # Log the activity
            log_activity(self.request.user, 'Create', f'Created case with ID {case.pk}')
            return redirect(self.success_url)  # Redirect to the success URL
        else:
            return HttpResponseForbidden("You do not have permission to assign yourself as case manager.")


@method_decorator([login_required, permission_required('app.change_case', raise_exception=True)], name='dispatch')
class CaseUpdateView(UpdateView):
    model = Case
    form_class = CaseForm
    template_name = 'cases/case_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated case with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.delete_case', raise_exception=True)], name='dispatch')
class CaseDeleteView(DeleteView):
    model = Case
    success_url = reverse_lazy('case_list')
    template_name = 'cases/case_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted case with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

@method_decorator([login_required, permission_required('app.add_casenote', raise_exception=True)], name='dispatch')
class CaseNoteCreateView(CreateView):
    model = CaseNote
    form_class = CaseNoteForm
    template_name = 'cases/case_note_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created case note with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.add_careplan', raise_exception=True)], name='dispatch')
class CarePlanCreateView(CreateView):
    model = CarePlan
    form_class = CarePlanForm
    template_name = 'cases/care_plan_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created care plan with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('app.view_careplan', raise_exception=True)], name='dispatch')
class CarePlanDetailView(DetailView):
    model = CarePlan
    template_name = 'cases/care_plan_detail.html'
    context_object_name = 'care_plan'
