from domain.base import BaseManager


class ChatManager(BaseManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    def prepare_list_queryset(self, queryset=None):
        return super().prepare_list_queryset(queryset).prefetch_related("messages")