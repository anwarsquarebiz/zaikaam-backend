from django.contrib import admin
from .models import Vendor, VendorUser, VendorWallet


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'rating', 'max_capacity', 'is_active')
    list_filter = ('city', 'is_active', 'rating')
    search_fields = ('name', 'city')
    list_editable = ('is_active',)
    ordering = ('name',)


@admin.register(VendorUser)
class VendorUserAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'user', 'role')
    list_filter = ('role', 'vendor')
    search_fields = ('vendor__name', 'user__username', 'user__email')
    raw_id_fields = ('vendor', 'user')
    ordering = ('vendor', 'user')


@admin.register(VendorWallet)
class VendorWalletAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'balance')
    search_fields = ('vendor__name',)
    raw_id_fields = ('vendor',)
    ordering = ('vendor',)
