from django.utils import timezone

from factory.django import DjangoModelFactory
from factory import LazyFunction
from factory.faker import Faker

from tests.base import BaseFactory


def fake_email_generator():
    return f"{Faker('user_name')}@{Faker('domain_name')}.com"

class UserFactory(DjangoModelFactory, BaseFactory):
    email = LazyFunction(fake_email_generator)
    password = "a@123456"
    is_verified = True
    is_active = True
    is_superuser = False
    is_staff = False
    is_hidden = False
    is_vip = False

    last_used_ip = Faker("ipv4")
    last_login = timezone.now()
    date_joined = timezone.now()

    class Meta:
        model = "identity.User"