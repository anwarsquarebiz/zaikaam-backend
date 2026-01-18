from rest_framework.permissions import BasePermission
from accounts.constants import (
    ROLE_ADMIN,
    ROLE_CUSTOMER,
    ROLE_VENDOR,
    ROLE_SUPPORT,
)


class IsAuthenticatedAndActive(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == ROLE_CUSTOMER
        )

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == ROLE_ADMIN
        )

class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == ROLE_VENDOR
        )

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == ROLE_SUPPORT
        )
