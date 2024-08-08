# from django.contrib import admin
# from .models import *
# # Register your models here.

# @admin.register(Bill)
# class BillAdmin(admin.ModelAdmin):
#     list_display = ('appointment', 'date_issued', 'total_amount', 'amount_paid', 'status', 'installment_plan')
#     search_fields = ('appointment__patient__profile__user__username', 'status')
#     list_filter = ('status', 'date_issued')


# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('bill', 'date_paid', 'amount', 'payment_method', 'installment')
#     search_fields = ('bill__appointment__patient__profile__user__username', 'payment_method')
#     list_filter = ('payment_method', 'date_paid')

