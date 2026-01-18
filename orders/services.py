from orders.models import Order, OrderStatusLog
from orders.tasks import assign_vendor_task


class OrderWorkflowService:

    @staticmethod
    def approve_order(order):
        order.status = 'approved'
        order.save()

        OrderStatusLog.objects.create(
            order=order,
            status='approved'
        )

        # ASYNC vendor assignment
        assign_vendor_task.delay(order.id)

        return order