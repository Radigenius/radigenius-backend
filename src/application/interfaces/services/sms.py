from typing import List
from datetime import datetime
from abc import ABC, abstractmethod
from django.db.models import QuerySet

from domain.apps.identity.models import User

from application.enums.services.enum import SMSTemplates


class ISMSService(ABC):
    @abstractmethod
    def param_generator(self, user: User, message: str, date: datetime) -> dict:
        pass

    @abstractmethod
    def bulk_param_generator(self, users: List[User] | QuerySet, message: str) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def lookup_param_generator(
        user: User, template: SMSTemplates, tokens: List[str]
    ) -> dict:
        pass

    @abstractmethod
    def send(self, user: User, message: str, date: datetime):
        pass

    @abstractmethod
    def bulk_send(self, users: List[User] | QuerySet, message: str):
        pass

    @abstractmethod
    def send_lookup(self, user: User, template: SMSTemplates, tokens: List[str]):
        pass

    @abstractmethod
    def send_bulk_lookup(
        self, users: List[User], template: SMSTemplates, tokens: List[str]
    ):
        pass

    @abstractmethod
    def send_to_all(self, template: SMSTemplates, tokens: List[str]):
        pass

    @abstractmethod
    def send_to_admins(self, template: SMSTemplates, tokens: List[str]):
        pass

    @abstractmethod
    def send_to_superuser(self, template: SMSTemplates, tokens: List[str]):
        pass

    @abstractmethod
    def send_otp(self, phone_number: str, template: SMSTemplates):
        pass

    @abstractmethod
    def send_register_success(self, user: User):
        pass

    @abstractmethod
    def send_ticket_created(self, user: User):
        pass

    @abstractmethod
    def send_ticket_answered(self, user: User):
        pass

    @abstractmethod
    def send_ticket_closed(self, user: User):
        pass

    @abstractmethod
    def send_product_available(self, users: List[User], product_title: str):
        pass

    @abstractmethod
    def send_coupon(self, user: User, code: str):
        pass

    @abstractmethod
    def send_admin_question_created(self, users: List[User]):
        pass

    @abstractmethod
    def send_admin_order_created(self):
        pass

    @abstractmethod
    def send_user_order_created(self, user: User, order_code: str):
        pass

    @abstractmethod
    def send_suspicious_activity(self, ip: str):
        pass
