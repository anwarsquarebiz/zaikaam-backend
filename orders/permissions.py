from rest_framework.permissions import BasePermission
from orders.models import VendorAssignment


class IsAssignedVendor(BasePermission):
    """
    Vendor can access ONLY orders assigned to them
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role != 'vendor':
            return False

        try:
            assignment = VendorAssignment.objects.get(order=obj)
            return assignment.vendor.vendoruser_set.filter(
                user=request.user
            ).exists()
        except VendorAssignment.DoesNotExist:
            return False
