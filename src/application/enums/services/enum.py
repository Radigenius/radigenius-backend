from enum import Enum

class CacheKeys(Enum):

    # Chat
    Chat_List = ("chat-list", 60 * 60 * 24)  # 1 day TTL

    @property
    def key(self):
        return self.value[0]

    @property
    def ttl(self):
        return self.value[1]
