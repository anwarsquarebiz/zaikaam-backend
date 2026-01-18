from django.contrib import admin
from .models import DeliveryTask, ProofOfDelivery


@admin.register(DeliveryTask)
class DeliveryTaskAdmin(admin.ModelAdmin):
    list_display = ('order', 'driver_name', 'status')
    list_filter = ('status',)
    search_fields = ('order__id', 'driver_name')
    raw_id_fields = ('order',)
    ordering = ('order',)


@admin.register(ProofOfDelivery)
class ProofOfDeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'otp_verified')
    list_filter = ('otp_verified',)
    search_fields = ('order__id',)
    raw_id_fields = ('order',)
    ordering = ('order',)
