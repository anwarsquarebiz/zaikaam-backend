from rest_framework import serializers
from decimal import Decimal
from .models import Order, OrderItem, OrderStatusLog, VendorAssignment
from menus.serializers import BrandMenuSerializer
from menus.models import BrandMenu
from vendors.models import Vendor


class OrderItemSerializer(serializers.ModelSerializer):
    menu = BrandMenuSerializer(read_only=True)
    menu_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ('menu', 'menu_id', 'quantity')


class OrderItemCreateSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CustomerOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'event_date',
            'guest_count',
            'status',
            'total_amount',
            'items',
            'created_at',
        )

class VendorOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'event_date',
            'guest_count',
            'status',
            'customer_name',
        )


class AdminVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'name', 'city')


class AdminOrderSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)

    def get_vendor(self, obj):
        assignment = getattr(obj, 'vendorassignment', None)
        if assignment:
            return AdminVendorSerializer(assignment.vendor).data
        return None

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'customer_name',
            'customer_email',
            'event_date',
            'guest_count',
            'status',
            'total_amount',
            'vendor',
            'items',
            'created_at',
        )
        read_only_fields = ('id', 'created_at', 'status')


class OrderCreateSerializer(serializers.Serializer):
    event_date = serializers.DateField()
    guest_count = serializers.IntegerField(min_value=1)
    items = OrderItemCreateSerializer(many=True, min_length=1)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        return value

    def validate_event_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past.")
        return value


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('placed', 'Placed'),
        ('approved', 'Approved'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('settled', 'Settled'),
        ('cancelled', 'Cancelled'),
    ])


class OrderStatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusLog
        fields = ('status', 'changed_at')
        read_only_fields = ('status', 'changed_at')
