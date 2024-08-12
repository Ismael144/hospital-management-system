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
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# Helper function to log activities
def log_activity(user, action, description):
    Activity.objects.create(user=user, action=action, description=description)

# Invoice Views
@method_decorator([login_required, permission_required('financials.view_invoice', raise_exception=True)], name='dispatch')
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10  # Adjust pagination as needed

@method_decorator([login_required, permission_required('financials.view_invoice', raise_exception=True)], name='dispatch')
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'

@method_decorator([login_required, permission_required('financials.add_invoice', raise_exception=True)], name='dispatch')
class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoice_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created invoice with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.change_invoice', raise_exception=True)], name='dispatch')
class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoice_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated invoice with ID {self.object.pk}')
        return response

# Expense Views
@method_decorator([login_required, permission_required('financials.view_expense', raise_exception=True)], name='dispatch')
class ExpenseListView(ListView):
    model = Expense
    template_name = 'financials/expense_list.html'
    context_object_name = 'expenses'

@method_decorator([login_required, permission_required('financials.view_expense', raise_exception=True)], name='dispatch')
class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'financials/expense_detail.html'

@method_decorator([login_required, permission_required('financials.add_expense', raise_exception=True)], name='dispatch')
class ExpenseCreateView(CreateView):
    model = Expense
    template_name = 'financials/expense_form.html'
    fields = ['category', 'amount', 'date', 'description', 'approved_by']
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created expense with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.change_expense', raise_exception=True)], name='dispatch')
class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'financials/expense_form.html'
    fields = ['category', 'amount', 'date', 'description', 'approved_by']
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated expense with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.delete_expense', raise_exception=True)], name='dispatch')
class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'financials/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted expense with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# Budget Views
@method_decorator([login_required, permission_required('financials.view_budget', raise_exception=True)], name='dispatch')
class BudgetListView(ListView):
    model = Budget
    template_name = 'financials/budget_list.html'
    context_object_name = 'budgets'

@method_decorator([login_required, permission_required('financials.view_budget', raise_exception=True)], name='dispatch')
class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'financials/budget_detail.html'

@method_decorator([login_required, permission_required('financials.add_budget', raise_exception=True)], name='dispatch')
class BudgetCreateView(CreateView):
    model = Budget
    template_name = 'financials/budget_form.html'
    fields = ['year', 'department', 'allocated_amount', 'spent_amount']
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created budget with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.change_budget', raise_exception=True)], name='dispatch')
class BudgetUpdateView(UpdateView):
    model = Budget
    template_name = 'financials/budget_form.html'
    fields = ['year', 'department', 'allocated_amount', 'spent_amount']
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated budget with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.delete_budget', raise_exception=True)], name='dispatch')
class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'financials/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted budget with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)

# FinancialReport Views
@method_decorator([login_required, permission_required('financials.view_financialreport', raise_exception=True)], name='dispatch')
class FinancialReportListView(ListView):
    model = FinancialReport
    template_name = 'financials/financial_report_list.html'
    context_object_name = 'reports'

@method_decorator([login_required, permission_required('financials.view_financialreport', raise_exception=True)], name='dispatch')
class FinancialReportDetailView(DetailView):
    model = FinancialReport
    template_name = 'financials/financial_report_detail.html'
    context_object_name = 'report'

@method_decorator([login_required, permission_required('financials.add_financialreport', raise_exception=True)], name='dispatch')
class FinancialReportCreateView(CreateView):
    model = FinancialReport
    template_name = 'financials/financial_report_form.html'
    fields = ['report_type', 'start_date', 'end_date', 'total_revenue', 'total_expenses', 'net_profit', 'generated_by', 'report_file']
    success_url = reverse_lazy('financial-report-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created financial report with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.change_financialreport', raise_exception=True)], name='dispatch')
class FinancialReportUpdateView(UpdateView):
    model = FinancialReport
    template_name = 'financials/financial_report_form.html'
    fields = ['report_type', 'start_date', 'end_date', 'total_revenue', 'total_expenses', 'net_profit', 'generated_by', 'report_file']
    success_url = reverse_lazy('financial-report-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated financial report with ID {self.object.pk}')
        return response

@method_decorator([login_required, permission_required('financials.delete_financialreport', raise_exception=True)], name='dispatch')
class FinancialReportDeleteView(DeleteView):
    model = FinancialReport
    template_name = 'financials/financial_report_confirm_delete.html'
    success_url = reverse_lazy('financial-report-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted financial report with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required


@method_decorator([login_required, permission_required('financials.view_insuranceprovider', raise_exception=True)], name='dispatch')
class InsuranceProviderListView(ListView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_list.html'
    context_object_name = 'insuranceproviders'


@method_decorator([login_required, permission_required('financials.view_insuranceprovider', raise_exception=True)], name='dispatch')
class InsuranceProviderDetailView(DetailView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_detail.html'
    context_object_name = 'insurance_provider'


@method_decorator([login_required, permission_required('financials.add_insuranceprovider', raise_exception=True)], name='dispatch')
class InsuranceProviderCreateView(CreateView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'contract_start_date', 'contract_end_date']
    success_url = reverse_lazy('insurance-provider-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created an insurance provider with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.change_insuranceprovider', raise_exception=True)], name='dispatch')
class InsuranceProviderUpdateView(UpdateView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address', 'contract_start_date', 'contract_end_date']
    success_url = reverse_lazy('insurance-provider-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated insurance provider with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.delete_insuranceprovider', raise_exception=True)], name='dispatch')
class InsuranceProviderDeleteView(DeleteView):
    model = InsuranceProvider
    template_name = 'financials/insurance_provider_confirm_delete.html'
    success_url = reverse_lazy('insurance-provider-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted insurance provider with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


@method_decorator([login_required, permission_required('financials.view_payroll', raise_exception=True)], name='dispatch')
class PayrollListView(ListView):
    model = Payroll
    template_name = 'payroll_list.html'


@method_decorator([login_required, permission_required('financials.view_payroll', raise_exception=True)], name='dispatch')
class PayrollDetailView(DetailView):
    model = Payroll
    template_name = 'payroll_detail.html'
    

@method_decorator([login_required, permission_required('financials.add_payroll', raise_exception=True)], name='dispatch')
class PayrollCreateView(CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'payroll_form.html'
    success_url = reverse_lazy('payroll_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new payroll entry with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.change_payroll', raise_exception=True)], name='dispatch')
class PayrollUpdateView(UpdateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'payroll_form.html'
    success_url = reverse_lazy('payroll_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated payroll entry with ID {self.object.pk}')
        return response
    

@method_decorator([login_required, permission_required('financials.delete_payroll', raise_exception=True)], name='dispatch')
class PayrollDeleteView(DeleteView):
    model = Payroll
    template_name = 'payroll_confirm_delete.html'
    success_url = reverse_lazy('payroll_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted payroll entry with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


@method_decorator([login_required, permission_required('financials.add_cashcollection', raise_exception=True)], name='dispatch')
class AccountListView(ListView):
    model = Account
    template_name = 'account_list.html'


@method_decorator([login_required, permission_required('financials.add_cashcollection', raise_exception=True)], name='dispatch')
class AccountDetailView(DetailView):
    model = Account
    template_name = 'account_detail.html'


@method_decorator([login_required, permission_required('financials.add_account', raise_exception=True)], name='dispatch')
class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new account with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.change_account', raise_exception=True)], name='dispatch')
class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'account_form.html'
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated account with ID {self.object.pk}')
        return response
    

@method_decorator([login_required, permission_required('financials.delete_account', raise_exception=True)], name='dispatch')
class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'account_confirm_delete.html'
    success_url = reverse_lazy('account_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted account with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


@method_decorator([login_required, permission_required('financials.view_cashcollection', raise_exception=True)], name='dispatch')
class CashCollectionListView(ListView):
    model = CashCollection
    template_name = 'cashcollection_list.html'
    context_object_name = "cashcollections"


@method_decorator([login_required, permission_required('financials.view_cashcollection', raise_exception=True)], name='dispatch')
class CashCollectionDetailView(DetailView):
    model = CashCollection
    template_name = 'cashcollection_detail.html'


@method_decorator([login_required, permission_required('financials.add_cashcollection', raise_exception=True)], name='dispatch')
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
        form.instance.collected_by = self.request.user
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new cash collection with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.change_cashcollection', raise_exception=True)], name='dispatch')
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
        form.instance.collected_by = self.get_object().collected_by
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated cash collection with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.delete_cashcollection', raise_exception=True)], name='dispatch')
class CashCollectionDeleteView(DeleteView):
    model = CashCollection
    template_name = 'cashcollection_confirm_delete.html'
    success_url = reverse_lazy('cashcollection_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted cash collection with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


@method_decorator([login_required, permission_required('financials.view_bill', raise_exception=True)], name='dispatch')
class BillListView(ListViewMixin, ListView):
    model = Bill
    template_name = 'bill_list.html'
    context_object_name = 'bills'


@method_decorator([login_required, permission_required('financials.view_bill', raise_exception=True)], name='dispatch')
class BillDetailView(DetailViewMixin, DetailView):
    model = Bill
    template_name = 'bill_detail.html'
    context_object_name = 'bill'


@method_decorator([login_required, permission_required('financials.add_bill', raise_exception=True)], name='dispatch')
class BillCreateView(CreateView):
    model = Bill
    form_class = BillForm
    template_name = 'bill_form.html'
    success_url = reverse_lazy('bill_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new bill with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.change_bill', raise_exception=True)], name='dispatch')
class BillUpdateView(UpdateView):
    model = Bill
    form_class = BillForm
    template_name = 'bill_form.html'
    success_url = reverse_lazy('bill_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated bill with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.delete_bill', raise_exception=True)], name='dispatch')
class BillDeleteView(DeleteView):
    model = Bill
    template_name = 'bill_confirm_delete.html'
    success_url = reverse_lazy('bill_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted bill with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


@method_decorator([login_required, permission_required('financials.view_payment', raise_exception=True)], name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'


@method_decorator([login_required, permission_required('financials.view_payment', raise_exception=True)], name='dispatch')
class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'payment_detail.html'


@method_decorator([login_required, permission_required('financials.add_payment', raise_exception=True)], name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Create', f'Created a new payment with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.change_payment', raise_exception=True)], name='dispatch')
class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment_form.html'
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, 'Update', f'Updated payment with ID {self.object.pk}')
        return response


@method_decorator([login_required, permission_required('financials.delete_payment', raise_exception=True)], name='dispatch')
class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        log_activity(request.user, 'Delete', f'Deleted payment with ID {self.object.pk}')
        return super().delete(request, *args, **kwargs)


def financial_reports(request):
    # Dummy data for now
    total_revenue = 100000
    total_expenses = 80000
    receivable_amount = 50000
    payable_amount = 25000
    budgets = [
        {'year': 2021, 'allocated_amount': 80000, 'spent_amount': 60000},
        {'year': 2022, 'allocated_amount': 90000, 'spent_amount': 75000},
        {'year': 2023, 'allocated_amount': 100000, 'spent_amount': 85000},
        {'year': 2024, 'allocated_amount': 110000, 'spent_amount': 95000},
        {'year': 2025, 'allocated_amount': 120000, 'spent_amount': 105000},
    ]
    pending_payroll_count = 1
    paid_payroll_count = 1

    context = {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'receivable_amount': receivable_amount,
        'payable_amount': payable_amount,
        'budgets': budgets,
        'pending_payroll_count': pending_payroll_count,
        'paid_payroll_count': paid_payroll_count,
        'accounts': [
            {'name': 'Accounts Receivable', 'amount': 50000, 'status': 'Pending'},
            {'name': 'Accounts Payable', 'amount': 25000, 'status': 'Pending'}
        ],
        'payrolls': [
            {'employee': 'John Doe', 'month': 'June 2023', 'net_pay': 5000, 'status': 'Paid'},
            {'employee': 'Jane Smith', 'month': 'June 2023', 'net_pay': 4500, 'status': 'Pending'}
        ]
    }
    return render(request, 'reports_analysis.html', context)
