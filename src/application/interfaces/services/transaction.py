from abc import ABC, abstractmethod
from domain.apps.store.models import Order, Transaction
from uuid import UUID


class ITransactionService(ABC):
    base_url: str
    callback_url: str
    api_key: str
    transaction = None

    @abstractmethod
    def generate(self) -> dict | Transaction:
        pass

    @abstractmethod
    def payment_start(self):
        pass

    @abstractmethod
    def payment_return(self, request):
        pass

    @abstractmethod
    def payment_check(self, transaction_id: UUID):
        pass
