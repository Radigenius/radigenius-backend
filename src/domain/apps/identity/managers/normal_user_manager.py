from .user_manager import UserManager


class NormalUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False, is_staff=False, is_hidden=False, is_vip=False)
