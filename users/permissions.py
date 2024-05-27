from rest_framework.permissions import BasePermission


class IsUserAdmDRF(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Администраторы DRF').exists:
            return True
        return False


class IsUserOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsUserUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
