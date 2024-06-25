from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """Пермишн для доступа только админу или суперюзеру."""
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        if user.is_authenticated:
            return (user.is_admin or user.is_superuser)


class AdminOrAuthorOrReadOnly(permissions.BasePermission):
    """Пермишн для доступа модератору, админу или автору."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin or request.user.is_moderator
                or request.user.is_superuser
                or request.user == obj.author)
