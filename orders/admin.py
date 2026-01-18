from django.contrib import admin
from .models import Order, OrderItem, VendorAssignment, OrderStatusLog


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ('menu',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'event_date', 'guest_count', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'event_date', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'id')
    raw_id_fields = ('customer',)
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu', 'quantity')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'menu__name')
    raw_id_fields = ('order', 'menu')
    ordering = ('order',)


@admin.register(VendorAssignment)
class VendorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'vendor', 'assigned_at')
    list_filter = ('vendor', 'assigned_at')
    search_fields = ('order__id', 'vendor__name')
    raw_id_fields = ('order', 'vendor')
    date_hierarchy = 'assigned_at'
    ordering = ('-assigned_at',)
    readonly_fields = ('assigned_at',)


@admin.register(OrderStatusLog)
class OrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_at')
    list_filter = ('status', 'changed_at')
    search_fields = ('order__id',)
    raw_id_fields = ('order',)
    date_hierarchy = 'changed_at'
    ordering = ('-changed_at',)
    readonly_fields = ('changed_at',)
