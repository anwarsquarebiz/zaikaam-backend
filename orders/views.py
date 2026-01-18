from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import Order, OrderItem, OrderStatusLog, VendorAssignment
from .serializers import (
    CustomerOrderSerializer,
    VendorOrderSerializer,
    AdminOrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
    OrderStatusLogSerializer,
)
from .services import OrderWorkflowService
from .tasks import update_order_status as update_order_status_task
from accounts.permissions import IsCustomer, IsVendor, IsAdmin
from .permissions import IsAssignedVendor
from menus.models import BrandMenu


class CustomerOrderCreateView(CreateAPIView):
    """
    Customer creates a new order
    """
    permission_classes = [IsCustomer]
    serializer_class = OrderCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        items_data = validated_data.pop('items')

        # Calculate total amount
        total_amount = Decimal('0.00')
        menu_ids = [item['menu_id'] for item in items_data]
        
        # Fetch menus and validate
        menus = {menu.id: menu for menu in BrandMenu.objects.filter(
            id__in=menu_ids,
            is_active=True
        )}
        
        if len(menus) != len(menu_ids):
            return Response(
                {"error": "Some menu items are invalid or inactive"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total
        for item_data in items_data:
            menu = menus[item_data['menu_id']]
            total_amount += menu.base_price * Decimal(str(item_data['quantity']))

        # Create order
        order = Order.objects.create(
            customer=request.user,
            event_date=validated_data['event_date'],
            guest_count=validated_data['guest_count'],
            total_amount=total_amount,
            status='placed'
        )

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                menu=menus[item_data['menu_id']],
                quantity=item_data['quantity']
            )

        # Log status
        OrderStatusLog.objects.create(
            order=order,
            status='placed'
        )

        response_serializer = CustomerOrderSerializer(order)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class CustomerOrderListView(ListAPIView):
    """
    List all orders for the authenticated customer
    """
    serializer_class = CustomerOrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')


class CustomerOrderDetailView(RetrieveAPIView):
    """
    Retrieve order details for customer
    """
    serializer_class = CustomerOrderSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class VendorOrderListView(ListAPIView):
    """
    List all orders assigned to the authenticated vendor
    """
    serializer_class = VendorOrderSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        return Order.objects.filter(
            vendorassignment__vendor__vendoruser__user=self.request.user
        ).order_by('-created_at')


class VendorOrderDetailView(RetrieveAPIView):
    """
    Retrieve order details for vendor
    """
    serializer_class = VendorOrderSerializer
    permission_classes = [IsVendor, IsAssignedVendor]

    def get_queryset(self):
        return Order.objects.filter(
            vendorassignment__vendor__vendoruser__user=self.request.user
        )


class VendorOrderStatusUpdateView(UpdateAPIView):
    """
    Vendor updates order status
    """
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsVendor, IsAssignedVendor]

    def get_queryset(self):
        return Order.objects.filter(
            vendorassignment__vendor__vendoruser__user=self.request.user,
            status__in=['approved', 'preparing', 'ready']
        )

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        
        # Validate status transition
        allowed_transitions = {
            'approved': ['preparing'],
            'preparing': ['ready'],
            'ready': ['out_for_delivery'],
        }
        
        if order.status in allowed_transitions:
            if new_status not in allowed_transitions[order.status]:
                return Response(
                    {"error": f"Cannot change status from {order.status} to {new_status}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Update status
        old_status = order.status
        order.status = new_status
        order.save()

        # Log status change
        OrderStatusLog.objects.create(
            order=order,
            status=new_status
        )

        # Use async task if needed
        update_order_status_task.delay(order.id, new_status)

        return Response({
            "message": f"Order status updated from {old_status} to {new_status}",
            "order": VendorOrderSerializer(order).data
        })


class AdminOrderListView(ListAPIView):
    """
    List all orders for admin
    """
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = Order.objects.all().select_related('customer').prefetch_related(
            'orderitem_set__menu',
            'vendorassignment__vendor'
        )
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')


class AdminOrderDetailView(RetrieveAPIView):
    """
    Retrieve order details for admin
    """
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdmin]
    queryset = Order.objects.all()


class ApproveOrderView(APIView):
    """
    Admin approves an order and assigns vendor
    """
    permission_classes = [IsAdmin]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            
            if order.status != 'placed':
                return Response(
                    {"error": f"Order is already {order.status}. Only 'placed' orders can be approved."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            OrderWorkflowService.approve_order(order)
            
            response_serializer = AdminOrderSerializer(order)
            return Response(
                {
                    "message": "Order approved and vendor assignment initiated",
                    "order": response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CancelOrderView(APIView):
    """
    Customer cancels their order (only if order is still 'placed' or 'approved')
    """
    permission_classes = [IsCustomer]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            
            # Only allow cancellation if order is placed or approved
            if order.status not in ['placed', 'approved']:
                return Response(
                    {"error": f"Cannot cancel order. Current status: {order.status}. Only 'placed' or 'approved' orders can be cancelled."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update status to cancelled (Note: 'cancelled' is not in STATUS_CHOICES but will work)
            # For production, consider adding 'cancelled' to STATUS_CHOICES in the model
            order.status = 'cancelled'
            order.save(update_fields=['status'])

            # Log status change
            OrderStatusLog.objects.create(
                order=order,
                status='cancelled'
            )

            return Response(
                {
                    "message": "Order cancelled successfully",
                    "order": CustomerOrderSerializer(order).data
                },
                status=status.HTTP_200_OK
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class OrderStatusHistoryView(ListAPIView):
    """
    Get status history for an order
    """
    serializer_class = OrderStatusLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        
        # Check permissions
        user = self.request.user
        if user.role == 'customer':
            if order.customer != user:
                return OrderStatusLog.objects.none()
        elif user.role == 'vendor':
            if not VendorAssignment.objects.filter(
                order=order,
                vendor__vendoruser__user=user
            ).exists():
                return OrderStatusLog.objects.none()
        # Admin can see all
        
        return OrderStatusLog.objects.filter(order=order).order_by('changed_at')
