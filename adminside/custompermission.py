from rest_framework.permissions import BasePermission,IsAuthenticated
from rest_framework.decorators import permission_classes




class OnlyAdminPermission(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        if current_user.is_admin:
            return True
        return False