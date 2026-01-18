from rest_framework import serializers
from .models import BrandMenu, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'image',
            'is_active',
            'display_order',
        )


class BrandMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandMenu
        fields = (
            'id',
            'category',
            'image',            
            'name',
            'description',
            'base_price',
        )

from .models import VendorMenu

class VendorMenuAdminSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(source='vendor.id', read_only=True)

    class Meta:
        model = VendorMenu
        fields = (
            'id',
            'vendor_id',
            'name',
            'is_approved',
        )
