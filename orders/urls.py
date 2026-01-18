from django.urls import path
from .views import (
    # Customer views
    CustomerOrderCreateView,
    CustomerOrderListView,
    CustomerOrderDetailView,
    CancelOrderView,
    
    # Vendor views
    VendorOrderListView,
    VendorOrderDetailView,
    VendorOrderStatusUpdateView,
    
    # Admin views
    AdminOrderListView,
    AdminOrderDetailView,
    ApproveOrderView,
    
    # Common views
    OrderStatusHistoryView,
)

urlpatterns = [
    # Customer endpoints
    path('customer/orders/', CustomerOrderListView.as_view(), name='customer-orders-list'),
    path('customer/orders/create/', CustomerOrderCreateView.as_view(), name='customer-orders-create'),
    path('customer/orders/<int:pk>/', CustomerOrderDetailView.as_view(), name='customer-orders-detail'),
    path('customer/orders/<int:order_id>/cancel/', CancelOrderView.as_view(), name='customer-orders-cancel'),
    
    # Vendor endpoints
    path('vendor/orders/', VendorOrderListView.as_view(), name='vendor-orders-list'),
    path('vendor/orders/<int:pk>/', VendorOrderDetailView.as_view(), name='vendor-orders-detail'),
    path('vendor/orders/<int:pk>/status/', VendorOrderStatusUpdateView.as_view(), name='vendor-orders-status-update'),
    
    # Admin endpoints
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-orders-list'),
    path('admin/orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-orders-detail'),
    path('admin/orders/<int:order_id>/approve/', ApproveOrderView.as_view(), name='admin-orders-approve'),
    
    # Common endpoints
    path('orders/<int:order_id>/history/', OrderStatusHistoryView.as_view(), name='order-status-history'),
]
