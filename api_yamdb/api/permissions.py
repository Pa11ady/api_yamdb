from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_authenticated:
            return user.role == 'admin'