from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    """BasePermission class adds all permissions for superUsers"""

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_superuser)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser)

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_superuser)


class IsOwnerOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        parent_access = super().has_object_permission(request, view, obj)
        return parent_access or obj.author == request.user.id

    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access or bool(request.user and request.user.is_authenticated)


class IsAdminUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access and bool(request.user and request.user.is_staff)


class IsVerified(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        parent_access = super().has_permission(request, view)
        return parent_access and bool(request.user and request.user.is_verified)


class CurrentUserOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user

        user_object = None
        if hasattr(obj, "user"):
            user_object = obj.user
        elif hasattr(obj, "profile") and hasattr(obj.profile, "user"):
            user_object = obj.profile.user

        return (
            user.is_superuser
            or user.is_staff
            or (user_object is not None and user_object.pk == user.pk)
        )
