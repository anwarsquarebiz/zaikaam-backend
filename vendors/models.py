from django.db import models
from accounts.models import User


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    max_capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class VendorUser(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('kitchen', 'Kitchen'),
        ('delivery', 'Delivery'),
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class VendorWallet(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
