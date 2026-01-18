from django.contrib import admin
from .models import Payment, Settlement


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'status', 'gateway', 'created_at')
    list_filter = ('status', 'gateway', 'created_at')
    search_fields = ('order__id', 'gateway')
    raw_id_fields = ('order',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'amount', 'settled_at')
    list_filter = ('settled_at',)
    search_fields = ('vendor__name',)
    raw_id_fields = ('vendor',)
    date_hierarchy = 'settled_at'
    ordering = ('-settled_at',)
