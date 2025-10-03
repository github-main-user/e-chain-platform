from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """Предоставляет доступ только активным сотрудникам."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)
