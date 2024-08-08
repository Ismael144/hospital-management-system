from .models import Notification

def send_notification(user, content, icon='fa-bell', link=None, link_name=None, bg_color=""):
    Notification.objects.create(
        user=user,
        content=content,
        icon=icon,
        link=link,
        link_name=link_name,
        bg_color=bg_color
    )