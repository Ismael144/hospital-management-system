from django.urls import path 
from .views import *

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('sent/', sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', message_detail, name='message_detail'),
    path('compose/', compose_message, name='send_message'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/mark/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('user-notifications-messages/', UserNotificationsMessagesView.as_view(), name='user_notifications_messages'),
    path('inbox/delete/<int:message_id>/', delete_inbox_message, name='message_inbox_delete'),
    path('messaging/clear-notifications/', ClearNotificationsView.as_view(), name='clear_notifications'),
    path('sent/delete/<int:message_id>/', delete_sent_message, name='message_sent_delete'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail')
]