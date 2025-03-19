from functools import wraps

from infrastructure.exceptions.exceptions import PermissionDeniedException


def check_permissions(permission_classes):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, *args, **kwargs):
            for permission_class in permission_classes:
                permission = permission_class()
                if not permission.has_permission(self.request, self):
                    raise PermissionDeniedException()

            return view_func(self, *args, **kwargs)

        return wrapper

    return decorator
