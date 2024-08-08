from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue')
    ]

    invoice_number = models.CharField(max_length=20, unique=True)
    bill = models.ForeignKey('Bill', on_delete=models.CASCADE, related_name='invoices')
    date_issued = models.DateField(default=timezone.now)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.bill}"

    def calculate_total_amount(self):
        if self.bill:
            self.total_amount = self.bill.total_amount - self.bill.amount_paid
        else:
            self.total_amount = 0
        return self.total_amount

    def save(self, *args, **kwargs):
        self.calculate_total_amount()
        self.clean()  # Ensure validation is run
        super().save(*args, **kwargs)

    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status != 'Paid'

    def mark_as_paid(self):
        self.status = 'Paid'
        self.save()


class Bill(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'), 
        ('Paid', 'Paid'), 
        ('Installments', 'Installments')
    ]

    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE)
    medication = models.ManyToManyField('pharmacy.Medication')
    date_issued = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    details = models.TextField()
    installment_plan = models.BooleanField(default=False)
    installments_remaining = models.IntegerField(default=0)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance_provider = models.ForeignKey('InsuranceProvider', on_delete=models.SET_NULL, null=True, blank=True)
    insurance_claim_status = models.CharField(max_length=50, choices=[
        ('Not Applicable', 'Not Applicable'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], default='Not Applicable')

    def __str__(self):
        return f"Bill for {self.appointment}"

    def update_status(self):
        if self.is_completed():
            self.status = 'Paid'
        elif self.installment_plan and self.installments_remaining > 0:
            self.status = 'Installments'
        else:
            self.status = 'Pending'
        self.save()

    def is_completed(self):
        return self.amount_paid >= self.total_amount

    def get_balance(self):
        return max(self.total_amount - self.amount_paid, 0)

    def record_payment(self, amount, payment_method, installment=False):
        if amount > self.get_balance():
            raise ValueError('Payment amount exceeds the remaining balance.')
        Payment.objects.create(
            bill=self,
            amount=amount,
            payment_method=payment_method,
            installment=installment
        )
        self.amount_paid += amount
        self.update_status()
        self.save()


class Payroll(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    
    def calculate_net_pay(self):
        overtime_pay = self.overtime_hours * self.overtime_rate
        self.net_pay = self.salary + overtime_pay + self.bonuses - self.deductions
        return self.net_pay
    
    def save(self, *args, **kwargs):
        self.calculate_net_pay()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Payroll for {self.employee.get_full_name()} - {self.month.strftime('%B %Y')}"


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Receivable', 'Receivable'),
        ('Payable', 'Payable')
    ]
    
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Settled', 'Settled')], default='Pending')
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.account_type}"


class CashCollection(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Mobile Money', 'Mobile Money'),
    ]
    
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    date_collected = models.DateField(auto_now_add=True)
    collected_by = models.ForeignKey("accounts.Accountant", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('Utilities', 'Utilities'),
        ('Supplies', 'Medical Supplies'),
        ('Equipment', 'Equipment'),
        ('Maintenance', 'Maintenance'),
        ('Salaries', 'Salaries'),
        ('Other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"


class Budget(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), 
        ('completed', 'Completed'), 
        ('cancelled', 'Cancelled'), 
    ]
    year = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Budget for {self.department} in {self.year}"

    def get_remaining_budget(self):
        return self.allocated_amount - self.spent_amount


class FinancialReport(models.Model):
    REPORT_TYPES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    ]
    
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2)
    generated_by = models.ForeignKey('accounts.Accountant', on_delete=models.SET_NULL, null=True)
    report_file = models.FileField(upload_to='financials/financial_reports/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.report_type} Report - {self.start_date} to {self.end_date}"


class InsuranceProvider(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Insurance', 'Insurance')])
    installment = models.BooleanField(default=False)
    processed_by = models.ForeignKey("accounts.Accountant", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Payment for {self.bill} - {self.amount}"

    def get_bill_balance(self):
        return self.bill.get_balance()

