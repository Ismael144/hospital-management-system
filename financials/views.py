from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Bill, Payment
from activities.models import Activity
from .forms import BillForm, PaymentForm
from mixins import *
from .models import Payroll, Account, CashCollection
from .forms import PayrollForm, AccountForm, CashCollectionForm, InvoiceForm
from django.shortcuts import render 
from .models import Expense, Budget, FinancialReport, InsuranceProvider, Invoice

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)
    

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10  # Adjust pagination as needed

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'

class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoice_list')

class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoice_list')

    
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'financials/expense_list.html'
    context_object_name = 'expenses'

class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'financials/expense_detail.html'

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'financials/expense_form.html'
    fields = ['category', 'amount', 'date', 'description', 'approved_by']
    success_url = reverse_lazy('expense-list')

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    template_name = 'financials/expense_form.html'
    fields = ['category', 'amount', 'date', 'description', 'approved_by']
    success_url = reverse_lazy('expense-list')

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'financials/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')

# Budget Views
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'financials/budget_list.html'
    context_object_name = 'budgets'

class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = 'financials/budget_detail.html'

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = 'financials/budget_form.html'
    fields = ['year', 'department', 'allocated_amount', 'spent_amount']
    success_url = reverse_lazy('budget-list')

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = 'financials/budget_form.html'
    fields = ['year', 'department', 'allocated_amount', 'spent_amount']
    success_url = reverse_lazy('budget-list')

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'financials/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')

# FinancialReport Views
class FinancialReportListView(LoginRequiredMixin, ListView):
    model = FinancialReport
    template_name = 'financials/financial_report_list.html'
    context_object_name = 'reports'

class FinancialReportDetailView(LoginRequiredMixin, DetailView):
    model = FinancialReport
    template_name = 'financials/financial_report_detail.html'
    context_object_name = 'report'

class FinancialReportCreateView(LoginRequiredMixin, CreateView):
    model = FinancialReport
    template_name = 'financials/financial_report_form.html'
    fields = ['report_type', 'start_date', 'end_date', 'total_revenue', 'total_expenses', 'net_profit', 'generated_by', 'report_file']
    success_url = reverse_lazy('financial-report-list')

class FinancialReportUpdateView(LoginRequiredMixin, UpdateView):
    model = FinancialReport
    template_name = 'financials/financial_report_form.html'
    fields = ['report_type', 'start_date', 'end_date', 'total_revenue', 'total_expenses', 'net_profit', 'generated_by', 'report_file']
    success_url = reverse_lazy('financial-report-list')

class FinancialReportDeleteView(LoginRequiredMixin, DeleteView):
    model = FinancialReport
    template_name = 'financials/financial_report_confirm_delete.html'
    success_url = reverse_lazy('financial-report-list')

# InsuranceProvider Views
class InsuranceProviderListView(LoginRequiredMixin, ListView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_list.html'
    context_object_name = 'insuranceproviders'

class InsuranceProviderDetailView(LoginRequiredMixin, DetailView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_detail.html'
    context_object_name = 'insurance_provider'

class InsuranceProviderCreateView(LoginRequiredMixin, CreateView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'contract_start_date', 'contract_end_date']
    success_url = reverse_lazy('insurance-provider-list')

class InsuranceProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'contract_start_date', 'contract_end_date']
    success_url = reverse_lazy('insurance-provider-list')

class InsuranceProviderDeleteView(LoginRequiredMixin, DeleteView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_confirm_delete.html'
    success_url = reverse_lazy('insurance-provider-list')
    
# Payroll Views
class PayrollListView(ListView):
    model = Payroll
    template_name = 'payroll_list.html'

class PayrollDetailView(DetailView):
    model = Payroll
    template_name = 'payroll_detail.html'

class PayrollCreateView(CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'payroll_form.html'
    success_url = reverse_lazy('payroll_list')

class PayrollUpdateView(UpdateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'payroll_form.html'
    success_url = reverse_lazy('payroll_list')

class PayrollDeleteView(DeleteView):
    model = Payroll
    template_name = 'payroll_confirm_delete.html'
    success_url = reverse_lazy('payroll_list')

# Account Views
class AccountListView(ListView):
    model = Account
    template_name = 'account_list.html'

class AccountDetailView(DetailView):
    model = Account
    template_name = 'account_detail.html'

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('account_list')

class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('account_list')

class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'account_confirm_delete.html'
    success_url = reverse_lazy('account_list')

# CashCollection Views
class CashCollectionListView(ListView):
    model = CashCollection
    template_name = 'cashcollection_list.html'
    context_object_name = "cashcollections"

class CashCollectionDetailView(DetailView):
    model = CashCollection
    template_name = 'cashcollection_detail.html'

class CashCollectionCreateView(CreateView):
    model = CashCollection
    form_class = CashCollectionForm
    template_name = 'cashcollection_form.html'
    success_url = reverse_lazy('cashcollection_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Set collected_by to the currently logged-in user
        form.instance.collected_by = self.request.user
        return super().form_valid(form)

class CashCollectionUpdateView(UpdateView):
    model = CashCollection
    form_class = CashCollectionForm
    template_name = 'cashcollection_form.html'
    success_url = reverse_lazy('cashcollection_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Ensure collected_by remains unchanged
        form.instance.collected_by = self.get_object().collected_by
        return super().form_valid(form)

class CashCollectionDeleteView(DeleteView):
    model = CashCollection
    template_name = 'cashcollection_confirm_delete.html'
    success_url = reverse_lazy('cashcollection_list')

# Bill views
class BillListView(ListViewMixin, ListView):
    model = Bill
    template_name = 'bill_list.html'
    context_object_name = 'bills'


class BillDetailView(DetailViewMixin, DetailView):
    model = Bill
    template_name = 'bill_detail.html'
    context_object_name = 'bill'

class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'bill_form.html'
    success_url = reverse_lazy('bill_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new bill with ID {self.object.pk}')
        return response

class BillUpdateView(UpdateView):
    model = Bill
    form_class = BillForm
    template_name = 'bill_form.html'
    success_url = reverse_lazy('bill_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated bill with ID {self.object.pk}')
        return response

class BillDeleteView(DeleteView):
    model = Bill
    template_name = 'bill_confirm_delete.html'
    success_url = reverse_lazy('bill_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted bill with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Payment views
class PaymentListView(ListViewMixin, ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'

class PaymentDetailView(DetailViewMixin, DetailView):
    model = Payment
    template_name = 'payment_detail.html'
    context_object_name = 'payment'

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new payment with ID {self.object.pk}')
        return response

class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated payment with ID {self.object.pk}')
        return response

class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted payment with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)
