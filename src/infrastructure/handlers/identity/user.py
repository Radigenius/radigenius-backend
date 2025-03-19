from django.contrib.auth import get_user_model
from django.utils import timezone

from infrastructure.handlers.base import BaseHandler
from infrastructure.exceptions.exceptions import (
    EntityNotFoundException,
    EntityAlreadyCreatedException,
)

User = get_user_model()


class UserHandler(BaseHandler):
    model = User

    def create(self, data):
        validated_data = self.validate(data)
        email = validated_data.get("email")

        try:
            user = self.model.objects.get_or_not_found_exception(email=email)
            raise EntityAlreadyCreatedException(entity_name="User")
        except EntityNotFoundException:
            return self.model.objects.create(**validated_data)

    def get_admins(self):
        return self.model.staffs.all()

    # @staticmethod
    # def ban(user_id, reason, until, description=""):
    #     try:
    #         return UserBan.objects.get_or_not_found_exception(user_id=user_id)
    #     except EntityNotFoundException:
    #         return UserBan.objects.create(
    #             user_id=user_id, reason=reason, until=until, description=description
    #         )

    # @staticmethod
    # def unban(user_id):
    #     return (
    #         UserBan.objects.all_objects()
    #         .filter(user_id=user_id)
    #         .update(until=timezone.now())
    #     )

    # @staticmethod
    # def is_banned(user_id):
    #     return UserBan.objects.filter(user_id=user_id).exists()
