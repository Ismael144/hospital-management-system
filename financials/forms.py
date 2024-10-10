from django import forms
from .models import Payroll, Account, CashCollection, Expense, Budget, FinancialReport, InsuranceProvider, Bill, Payment, Invoice
from appointments.models import Appointment

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_number',
            'bill',
            'due_date',
            'description',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'
        widgets = {
            'employee': forms.Select(),
            'month': forms.DateInput(attrs={'type': 'date'}),
            'salary': forms.NumberInput(attrs={'step': '0.01', 'value': 0}),
            'bonuses': forms.NumberInput(attrs={'step': '0.01'}),
            'deductions': forms.NumberInput(attrs={'step': '0.01'}),
            'status': forms.Select(),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'account_type': forms.Select(),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'status': forms.Select(),
            'description': forms.Textarea(),
        }

class CashCollectionForm(forms.ModelForm):
    class Meta:
        model = CashCollection
        fields = '__all__'
        widgets = {
            'payment_method': forms.Select(),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'date_collected': forms.DateInput(attrs={'type': 'date'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'category': forms.Select(),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(),
            'approved_by': forms.Select(),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'
        widgets = {
            'year': forms.NumberInput(),
            'allocated_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'spent_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'department': forms.Select(),
        }

class FinancialReportForm(forms.ModelForm):
    class Meta:
        model = FinancialReport
        fields = '__all__'
        widgets = {
            'report_type': forms.Select(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'total_revenue': forms.NumberInput(attrs={'step': '0.01'}),
            'total_expenses': forms.NumberInput(attrs={'step': '0.01'}),
            'net_profit': forms.NumberInput(attrs={'step': '0.01'}),
            'generated_by': forms.Select(),
            'report_file': forms.ClearableFileInput(),
        }


class InsuranceProviderForm(forms.ModelForm):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'
        widgets = {
            'contract_start_date': forms.DateInput(),
            'contract_end_date': forms.DateInput(),
            'email': forms.EmailInput(),
            'phone': forms.TextInput(),
            'address': forms.Textarea(),
        }


class BillForm(forms.ModelForm):
    set_amount_automatically = forms.BooleanField(
        required=False,
        label='Set total amount based on medications',
        initial=False,
    )

    class Meta:
        model = Bill
        fields = '__all__'
        widgets = {
            'appointment': forms.Select(),
            'medication': forms.SelectMultiple(),
            'date_issued': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'total_amount': forms.NumberInput(attrs={'step': '0.01', 'required': False}),
            'amount_paid': forms.NumberInput(attrs={'step': '0.01'}),
            'status': forms.Select(),
            'details': forms.Textarea(),
            'insurance_claim_status': forms.Select(),
        }
        
    def __init__(self, *args, **kwargs):
        appt_id = kwargs.pop('appt_id', None)
        super().__init__(*args, **kwargs)
        if appt_id:
            try:
                # Fetch the Appointment object using the appt_id
                appointment = Appointment.objects.get(pk=appt_id)
                # Set the initial value of the appointment field
                self.fields['appointment'].initial = appointment.id
            except Appointment.DoesNotExist:
                pass  
    
    def clean(self):
        cleaned_data = super().clean()
        set_amount_automatically = cleaned_data.get('set_amount_automatically')
        medications = cleaned_data.get('medication')
        total_amount = cleaned_data.get('total_amount')
        
        if set_amount_automatically and medications:
            # Calculate the total price of selected medications
            medication_total = sum(med.price for med in medications)
            # Add the calculated medication total to the entered total amount
            cleaned_data['total_amount'] = total_amount + medication_total
        
        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'bill': forms.Select(),
            'date_paid': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'payment_method': forms.Select(),
            'installment': forms.CheckboxInput(),
            'processed_by': forms.Select(),
        }

