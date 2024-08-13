from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from activities.models import Activity
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class LoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('signin_page')

# mixins.py
class ActivityLogMixin:
    def log_activity(self, user, action, model_name, object_id):
        Activity.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=object_id,
            timestamp=now()
        )

class ModelFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# Helper functions for create, update, and delete views
def create_view_helper(model, form_class, success_url, template_name):
    return CreateView.as_view(
        model=model,
        form_class=form_class,
        success_url=success_url,
        template_name=template_name
    )

def update_view_helper(model, form_class, success_url, template_name):
    return UpdateView.as_view(
        model=model,
        form_class=form_class,
        success_url=success_url,
        template_name=template_name
    )

def delete_view_helper(model, success_url, template_name):
    return DeleteView.as_view(
        model=model,
        success_url=success_url,
        template_name=template_name
    )

# List and Detail Views using a common mixin for simplicity
class ListViewMixin(ListView):
    model = None
    template_name = None
    context_object_name = None
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name_plural'] = self.model.__name__.lower() + 's'
        return context

class DetailViewMixin(DetailView):
    model = None
    template_name = None
    context_object_name = None
