from .user_manager import UserManager


class VIPUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_vip=True)
