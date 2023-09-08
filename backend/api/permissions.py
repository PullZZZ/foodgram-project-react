from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
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
