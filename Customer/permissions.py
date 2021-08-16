from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_staff:
            return True
        else:
            if request.user.is_superuser:
                return True


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner.user == request.user


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.phone == request.user.phone or request.user.is_staff:
            return True
        else:
            return False
