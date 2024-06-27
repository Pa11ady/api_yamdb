from rest_framework import permissions


class AnonReadOnly(permissions.BasePermission):
    """Разрешает методы GET, HEAD, OPTIONS анонимным пользователям."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserOrAdminAndIsAuth(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователю или администратору,
    если пользователь аутентифицирован.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_superuser or request.user.is_admin)


class IsSuperUserOrAdminOrModerOrAuthorAndIsAuth(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователю, администратору, модератору
    или автору объекта, если пользователь аутентифицирован.
    Разрешает методы GET, HEAD, OPTIONS для всех пользователей.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or any(
                (
                    request.user.is_superuser,
                    request.user.is_admin,
                    request.user.is_moderator,
                    request.user == obj.author,
                )
            )
        )
