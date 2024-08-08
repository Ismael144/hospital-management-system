document.addEventListener('DOMContentLoaded', function() {
    fetchNotificationsAndMessages();

    document.getElementById('mark-all-read').addEventListener('click', markAllAsRead);
});

function fetchNotificationsAndMessages() {
    fetch('/api/user/notifications-messages/')
        .then(response => response.json())
        .then(data => {
            displayNotifications(data.notifications);
            displayMessages(data.messages);
        })
        .catch(error => console.error('Error fetching notifications and messages:', error));
}

function displayNotifications(notifications) {
    const notificationsList = document.getElementById('notifications-list');
    notificationsList.innerHTML = '';

    notifications.forEach(notification => {
        const li = document.createElement('li');
        li.textContent = notification.content;
        li.className = notification.read ? 'read' : 'new';
        li.dataset.id = notification.id;
        notificationsList.appendChild(li);
    });
}

function displayMessages(messages) {
    const messagesList = document.getElementById('messages-list');
    messagesList.innerHTML = '';

    messages.forEach(message => {
        const li = document.createElement('li');
        li.textContent = message.content;
        li.className = message.read ? 'read' : 'new';
        li.dataset.id = message.id;
        messagesList.appendChild(li);
    });
}

function markAllAsRead() {
    const notificationIds = Array.from(document.querySelectorAll('#notifications-list .new'))
        .map(li => li.dataset.id);
    const messageIds = Array.from(document.querySelectorAll('#messages-list .new'))
        .map(li => li.dataset.id);

    fetch('api/user/notification-messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // CSRF token for Django
        },
        body: JSON.stringify({
            notifications: notificationIds,
            messages: messageIds
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Marked as read:', data);
        fetchNotificationsAndMessages();  // Refresh the lists
    })
    .catch(error => console.error('Error marking as read:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

displayMessages()
displayNotifications()