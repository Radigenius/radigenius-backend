from domain.base import BaseManager


class ChatManager(BaseManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)