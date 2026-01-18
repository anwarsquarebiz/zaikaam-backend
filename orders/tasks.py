from celery import shared_task
from orders.models import Order, OrderStatusLog
from vendors.services import VendorAssignmentService
from notifications.tasks import send_order_notification


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def assign_vendor_task(self, order_id):
    order = Order.objects.get(id=order_id)

    VendorAssignmentService.assign_vendor(order)

    OrderStatusLog.objects.create(
        order=order,
        status='vendor_assigned'
    )

    send_order_notification.delay(
        order.customer_id,
        "Order Approved",
        "Your order has been approved and is being prepared."
    )

@shared_task
def update_order_status(order_id, status):
    order = Order.objects.get(id=order_id)
    order.status = status
    order.save()

    OrderStatusLog.objects.create(
        order=order,
        status=status
    )