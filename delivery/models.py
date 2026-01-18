from django.db import models
from orders.models import Order


class DeliveryTask(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='assigned')


class ProofOfDelivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='delivery/')
    otp_verified = models.BooleanField(default=False)
