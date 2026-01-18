from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import BrandMenu, Category
from .serializers import BrandMenuSerializer, CategorySerializer
from accounts.permissions import IsCustomer


class CustomerMenuListView(ListAPIView):
    queryset = BrandMenu.objects.filter(is_active=True)
    serializer_class = BrandMenuSerializer
    permission_classes = [IsCustomer]


# Customer Menu List View grouped by category
class CustomerMenuListByCategoryView(ListAPIView):
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        # Get all active menus with their categories
        menus = BrandMenu.objects.filter(is_active=True).select_related('category').order_by(
            'category__display_order', 'category__name', 'name'
        )
        
        # Group menus by category
        grouped_data = {}
        uncategorized_menus = []
        
        for menu in menus:
            if menu.category:
                category_id = menu.category.id
                if category_id not in grouped_data:
                    grouped_data[category_id] = {
                        'category': menu.category,
                        'menus': []
                    }
                grouped_data[category_id]['menus'].append(menu)
            else:
                uncategorized_menus.append(menu)
        
        # Convert to list format using serializers
        result = []
        for category_id, data in sorted(grouped_data.items(), key=lambda x: (
            x[1]['category'].display_order, 
            x[1]['category'].name
        )):
            result.append({
                'category': CategorySerializer(data['category']).data,
                'menus': BrandMenuSerializer(data['menus'], many=True).data
            })
        
        # Add uncategorized items if any
        if uncategorized_menus:
            result.append({
                'category': None,
                'menus': BrandMenuSerializer(uncategorized_menus, many=True).data
            })
        
        return Response(result)

from rest_framework.generics import ListAPIView
from .models import VendorMenu
from .serializers import VendorMenuAdminSerializer
from accounts.permissions import IsAdmin


class AdminVendorMenuListView(ListAPIView):
    queryset = VendorMenu.objects.all()
    serializer_class = VendorMenuAdminSerializer
    permission_classes = [IsAdmin]
