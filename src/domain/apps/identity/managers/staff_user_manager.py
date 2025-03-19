from .user_manager import UserManager


class StaffUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)
