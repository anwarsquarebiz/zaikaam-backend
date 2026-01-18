from vendors.models import Vendor
from orders.models import VendorAssignment
from django.db import transaction


class VendorAssignmentService:
    """
    Handles vendor selection & assignment.
    White-label safe: customer never sees vendor.
    """

    @staticmethod
    def find_best_vendor(order):
        """
        Returns the best matching vendor for an order.
        """

        vendors = Vendor.objects.filter(
            city=order.customer.profile.city,
            is_active=True,
            max_capacity__gte=order.guest_count,
        ).order_by(
            '-rating',
            'max_capacity'
        )

        return vendors.first()

    @staticmethod
    @transaction.atomic
    def assign_vendor(order, force=False):
        """
        Assigns vendor to an order.
        If force=True, replaces existing vendor.
        """

        if not force and hasattr(order, 'vendorassignment'):
            return order.vendorassignment

        vendor = VendorAssignmentService.find_best_vendor(order)

        if not vendor:
            raise Exception("No vendor available for this order")

        assignment, created = VendorAssignment.objects.update_or_create(
            order=order,
            defaults={'vendor': vendor}
        )

        return assignment
