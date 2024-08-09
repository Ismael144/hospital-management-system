from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Patient, Nurse, Doctor, CaseManager, Representative

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'profile_image'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('address', 'phone_number', 'date_of_birth', 'emergency_contact_name', 'insurance_provider', 'status', 'disease', 'assigned_room')
#     search_fields = ('user__username', 'user__first_name', 'user__last_name', 'assigned_room__room_number')
#     list_filter = ('date_of_birth', 'insurance_provider', 'assigned_room', 'assigned_doctor__user__first_name')

#     fieldsets = (
#         (None, {
#             'fields': ('user', 'address', 'phone_number', 'date_of_birth', 'medical_history', 'assigned_room', 'assigned_doctor')
#         }),
#         (_('Emergency Contact'), {
#             'fields': ('emergency_contact_name', 'emergency_contact_phone')
#         }),
#         (_('Insurance Information'), {
#             'fields': ('insurance_provider', 'insurance_policy_number')
#         }),
#         (_('Medical Details'), {
#             'fields': ('allergies', 'current_medications', 'family_medical_history', 'health_habits')
#         }),
#         (_('More Details'), {
#             'fields': ('status', 'disease')
#         }),
#         (_('Preferences'), {
#             'fields': ('preferred_language',)
#         }),
#     )

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.select_related('user', 'assigned_doctor', 'assigned_room')
#         return queryset

#     def get_username(self, obj):
#         return obj.user.username

#     get_username.admin_order_field = 'user__username'

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('qualifications', 'years_of_experience')
    search_fields = ('profile__employee__user__email', 'profile__employee__user__first_name', 'profile__employee__user__last_name')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('specialization', 'years_of_experience', 'department')
    search_fields = ('profile__user__username', 'profile__user__first_name', 'profile__user__last_name', 'specialization', 'department')
    list_filter = ('specialization', 'department')

class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'date_hired')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'department')
    ordering = ('user__email',)

# admin.site.register(CaseManager)
# admin.site.register(Patient, PatientAdmin)
# admin.site.register(Nurse, NurseAdmin)
# admin.site.register(Representative, RepresentativeAdmin)
