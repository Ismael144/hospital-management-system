from django.contrib import admin
from .models import * 

# Register your models here.
# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'content', 'timestamp', 'read')
#     list_filter = ('read', 'timestamp')
#     search_fields = ('content', 'user__email')
#     ordering = ('-timestamp',)

# @admin.register(Message)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp', 'read')
    list_filter = ('read', 'timestamp')
    search_fields = ('content', 'sender__email', 'receiver__email')
    ordering = ('-timestamp',)
