from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_admin", False))


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_staff", False))


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_manager", False))


class CommitRolePermission(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        if not u or not u.is_authenticated:
            return False

        if getattr(u, "is_admin", False):
            return True

        if getattr(u, "is_staff", False):
            return request.method in (SAFE_METHODS | {"POST"})

        if getattr(u, "is_manager", False):
            return request.method in SAFE_METHODS

        return False
