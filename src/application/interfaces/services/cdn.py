from typing import Literal
from abc import ABC, abstractmethod

from domain.apps.identity.models import IPBan


class ICDNService(ABC):

    domain: str
    APIKEY: str
    headers: dict

    @abstractmethod
    def get_firewall_rule(self, cdn_ban_id: str):
        pass

    @abstractmethod
    def create_firewall_rule(self, entity: IPBan) -> IPBan:
        pass

    @abstractmethod
    def update_firewall_rule(self, ip: str, cdn_ban_id: str, action: Literal['remove_ip', 'add_ip']):
        pass
