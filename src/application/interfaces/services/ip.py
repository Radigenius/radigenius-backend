from django.http import HttpRequest
from abc import ABC, abstractmethod

from domain.apps.identity.models import User


class IIPService:

    @abstractmethod
    def get_client_ip(self, request: HttpRequest) -> str:
        pass

    @abstractmethod
    def get_user_ip(self, user: User) -> str:
        pass
