from django.urls import path
from .views import CustomerMenuListView, AdminVendorMenuListView, CustomerMenuListByCategoryView

urlpatterns = [
    path('customer/menus/', CustomerMenuListView.as_view()),
    path('customer/menus/category/', CustomerMenuListByCategoryView.as_view()),
    path('admin/vendor-menus/', AdminVendorMenuListView.as_view()),
]
