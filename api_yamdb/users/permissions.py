from rest_framework import permissions


class AnonReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserOrAdminAndIsAuth(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin)


class IsSuperUserOrAdminOrModerOrAuthorAndIsAuth(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)
        )
