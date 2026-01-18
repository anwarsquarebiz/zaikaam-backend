from celery import shared_task
from notifications.models import Notification
from accounts.models import User


@shared_task
def send_order_notification(user_id, title, message):
    user = User.objects.get(id=user_id)
    Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
