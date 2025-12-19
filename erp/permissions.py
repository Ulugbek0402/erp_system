from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="teacher").exists()


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="student").exists()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
