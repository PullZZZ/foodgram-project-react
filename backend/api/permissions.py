from rest_framework import permissions


class AuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа: запросы на изменение и удаление -
    только администратор или автор объекта.
    Остальные - только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
            or request.user == obj.author
        )


class CurrentUserOrAdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа: запросы на изменение и удаление -
    только администратор или сам пользователь.
    Остальные - только чтение.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, type(user)) and obj == user:
            return True
        return request.method in permissions.SAFE_METHODS or user.is_staff
