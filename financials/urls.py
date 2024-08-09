from django.urls import path 
from .views import *

urlpatterns = [
    # Invoice URLs
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice_update'), 
    
    # Bill URLs
    path('bills/', BillListView.as_view(), name='bill_list'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill_detail'),
    path('bills/new/', BillCreateView.as_view(), name='bill_create'),
    path('bills/<int:pk>/edit/', BillUpdateView.as_view(), name='bill_update'),
    path('bills/<int:pk>/delete/', BillDeleteView.as_view(), name='bill_delete'),

    # Payment URLs
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/new/', PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/edit/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
    
    # Payroll URLs
    path('payroll/', PayrollListView.as_view(), name='payroll_list'),
    path('payroll/<int:pk>/', PayrollDetailView.as_view(), name='payroll_detail'),
    path('payroll/new/', PayrollCreateView.as_view(), name='payroll_create'),
    path('payroll/<int:pk>/edit/', PayrollUpdateView.as_view(), name='payroll_update'),
    path('payroll/<int:pk>/delete/', PayrollDeleteView.as_view(), name='payroll_delete'),

    # Account URLs
    path('account/', AccountListView.as_view(), name='account_list'),
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('account/new/', AccountCreateView.as_view(), name='account_create'),
    path('account/<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update'),
    path('account/<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),

    # CashCollection URLs
    path('cashcollection/', CashCollectionListView.as_view(), name='cashcollection_list'),
    path('cashcollection/<int:pk>/', CashCollectionDetailView.as_view(), name='cashcollection_detail'),
    path('cashcollection/new/', CashCollectionCreateView.as_view(), name='cashcollection_create'),
    path('cashcollection/<int:pk>/edit/', CashCollectionUpdateView.as_view(), name='cashcollection_update'),
    path('cashcollection/<int:pk>/delete/', CashCollectionDeleteView.as_view(), name='cashcollection_delete'),

    # Expense URLs
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/new/', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
    
    # Budget URLs
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path('budgets/new/', BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget-update'),
    path('budgets/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget-delete'),
    
    # FinancialReport URLs
    path('reports/', FinancialReportListView.as_view(), name='financial-report-list'),
    path('reports/<int:pk>/', FinancialReportDetailView.as_view(), name='financial-report-detail'),
    path('reports/new/', FinancialReportCreateView.as_view(), name='financial-report-create'),
    path('reports/<int:pk>/edit/', FinancialReportUpdateView.as_view(), name='financial-report-update'),
    path('reports/<int:pk>/delete/', FinancialReportDeleteView.as_view(), name='financial-report-delete'),
    
    # InsuranceProvider URLs
    path('insurance-providers/', InsuranceProviderListView.as_view(), name='insurance-provider-list'),
    path('insurance-providers/<int:pk>/', InsuranceProviderDetailView.as_view(), name='insurance-provider-detail'),
    path('insurance-providers/new/', InsuranceProviderCreateView.as_view(), name='insurance-provider-create'),
    path('insurance-providers/<int:pk>/edit/', InsuranceProviderUpdateView.as_view(), name='insurance-provider-update'),
    path('insurance-providers/<int:pk>/delete/', InsuranceProviderDeleteView.as_view(), name='insurance-provider-delete'),

    path('reports_analysis', financial_reports, name='insurance-provider-delete'),
]
