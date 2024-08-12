import json
from django.db.models import Q
from .forms import MessageForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import View
from .models import Message, Notification
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView


class SignInRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('signin_page')

class UserNotificationsMessagesView(SignInRequiredMixin, View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        messages = Message.objects.filter(receiver=request.user)
        
        notifications_data = [
            {
                "id": notification.pk,
                "content": notification.content,
                "timestamp": notification.timestamp,
                "read": notification.read,
                "icon": notification.icon,  # Include additional fields if needed
                "link": notification.link,
                "bg_color": notification.bg_color,
                "link_name": notification.link_name,
            } 
            for notification in notifications
        ]
        
        messages_data = [
            {
                "id": message.pk,
                "content": message.content,
                "timestamp": message.timestamp,
                "read": message.read,
            }
            for message in messages
        ]
        
        data = {
            "notifications": notifications_data,
            "messages": messages_data,
        }
        
        return JsonResponse(data)

    def post(self, request):
        try:
            body = json.loads(request.body)
            notification_ids = body.get('notifications', [])
            message_ids = body.get('messages', [])
        except (json.JSONDecodeError, KeyError) as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")

        if notification_ids:
            Notification.objects.filter(id__in=notification_ids, user=request.user).update(read=True)
        if message_ids:
            Message.objects.filter(id__in=message_ids, receiver=request.user).update(read=True)

        return JsonResponse({"status": "success"})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'messaging/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    return redirect('notifications')


@method_decorator(csrf_exempt, name='dispatch')
class ClearNotificationsView(View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            notification_ids = body.get('notifications', [])
        except (json.JSONDecodeError, KeyError) as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")

        if notification_ids:
            Notification.objects.filter(id__in=notification_ids, user=request.user).update(read=True)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "success"})


class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notifications/notification_detail.html'
    context_object_name = 'notification'
    
    def get_queryset(self):
        # Ensure only the receiver can view their notifications
        return Notification.objects.filter(user=self.request.user)


@login_required
def inbox(request):
    query = request.GET.get('q')
    filter = request.GET.get('filter')  # Get the read/unread filter
    
    received_messages = Message.objects.filter(receiver=request.user)

    if query:
        received_messages = received_messages.filter(content__icontains=query)
    
    if filter == 'read':
        received_messages = received_messages.filter(read=True)
    elif filter == 'unread':
        received_messages = received_messages.filter(read=False)
    
    received_messages = received_messages.order_by('-timestamp')

    paginator = Paginator(received_messages, 10)  # Show 10 messages per page
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    
    context = {
        'messages': messages,
        'inbox_count': Message.objects.filter(receiver=request.user).count(),
        'sent_count': Message.objects.filter(sender=request.user).count(),
        'query': query,
        'read_filter': filter,  
    }
    return render(request, 'messaging/inbox.html', context)



@login_required
def sent_messages(request):
    query = request.GET.get('q')
    read_filter = request.GET.get('filter')  # Get the read/unread filter

    sent_messages = Message.objects.filter(sender=request.user)

    if query:
        sent_messages = sent_messages.filter(Q(content__icontains=query) | Q(subject__icontains=query))
    
    if read_filter == 'read':
        sent_messages = sent_messages.filter(read=True)
    elif read_filter == 'unread':
        sent_messages = sent_messages.filter(read=False)

    sent_messages = sent_messages.order_by('-timestamp')

    paginator = Paginator(sent_messages, 10)  # Show 10 messages per page
    page = request.GET.get('page')
    try:
        messages_page = paginator.page(page)
    except PageNotAnInteger:
        messages_page = paginator.page(1)
    except EmptyPage:
        messages_page = paginator.page(paginator.num_pages)
    
    context = {
        'messages': messages_page,
        'inbox_count': Message.objects.filter(receiver=request.user).count(),
        'sent_count': sent_messages.count(),
        'query': query,
        'read_filter': read_filter,
    }
    return render(request, 'messaging/sent_messages.html', context)


@login_required
def compose_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            print(Message.objects.all())
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
        else:
            messages.error(request, 'There was an error with your form submission.')
            print(form.errors)  # Add this line to print form errors to the console for debugging
    else:
        form = MessageForm()
        
    context = { 'form': form, 
                'inbox_count': Message.objects.filter(receiver=request.user).count(),
                'sent_count': Message.objects.filter(sender=request.user).count()
    }
    return render(request, 'messaging/send_message.html', context)


@login_required
def delete_inbox_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    
    if request.user != message.receiver and request.user != message.sender:
        messages.error(request, "You do not have permission to view this message.")
        return reverse_lazy("inbox")

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully.')
        return redirect('inbox')
    return redirect('inbox')


@login_required
def delete_sent_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    if request.user != message.receiver and request.user != message.sender:
        messages.error(request, "You do not have permission to view this message.")
        return redirect("inbox")

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Sent message deleted successfully.')
        return redirect('sent_messages')
    return redirect('sent_messages')


@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if not message.read and message.receiver == request.user: 
        message.read = True 
        message.save()
        
    if request.user != message.receiver and request.user != message.sender:
        messages.error(request, "You do not have permission to view this message.")
        return redirect("inbox")

    if request.user == message.receiver and not message.read:
        message.read = True
        message.save()

    context = {
        'message': message,
        'inbox_count': Message.objects.filter(receiver=request.user).count(),
        'sent_count': Message.objects.filter(sender=request.user).count(),
    }

    return render(request, 'messaging/message_detail.html', context)
