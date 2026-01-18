from django.db import models
from accounts.models import User
from vendors.models import Vendor
from menus.models import BrandMenu


class Order(models.Model):
    STATUS_CHOICES = (
        ('placed', 'Placed'),
        ('approved', 'Approved'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('settled', 'Settled'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateField()
    guest_count = models.PositiveIntegerField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='placed')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(BrandMenu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class VendorAssignment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)


class OrderStatusLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    changed_at = models.DateTimeField(auto_now_add=True)
