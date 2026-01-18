from django.db import models
from orders.models import Order
from vendors.models import Vendor


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30)
    gateway = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Settlement(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    settled_at = models.DateTimeField(null=True, blank=True)
