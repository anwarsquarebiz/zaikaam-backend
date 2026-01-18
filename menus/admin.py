from django.contrib import admin
from .models import Category, VendorMenu, BrandMenu


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order', 'name')


@admin.register(VendorMenu)
class VendorMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'is_approved')
    list_filter = ('is_approved', 'vendor')
    search_fields = ('name', 'vendor__name')
    list_editable = ('is_approved',)
    raw_id_fields = ('vendor',)
    ordering = ('vendor', 'name')


@admin.register(BrandMenu)
class BrandMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    raw_id_fields = ('category',)
    ordering = ('category', 'name')
