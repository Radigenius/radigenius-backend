from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status

# from domain.apps.identity.models import User, UserBan
from infrastructure.commands.base import BaseCommand
from infrastructure.handlers.identity.user import UserHandler
from infrastructure.exceptions.exceptions import ValidationException
from infrastructure.services.token import TokenService
from infrastructure.services.mail import MailService
from domain.apps.identity.models import OTP, User
from application.enums.services.enum import EmailTemplates


class UserCommand(BaseCommand):
    handler = UserHandler

    # def _check_user_ban(self, user):
    #     ban_entity = UserBan.objects.filter(user_id=user.id)
    #     if ban_entity.exists():
    #         raise UserBanException(
    #             errors=[
    #                 {
    #                     "until": ban_entity[0].until,
    #                     "reason": ban_entity[0].reason,
    #                     "description": ban_entity[0].description,
    #                 }
    #             ]
    #         )

    def create(self, data):

        validated_data = self.validate(data)
        handler = self.handler(self.view, self.request)
        
        email = validated_data.get("email")
        otp = validated_data.pop("otp")
        
        OTP.objects.verify(email=email, code=otp)

        validated_data["is_verified"] = True
        user = handler.create(validated_data)

        token_service = TokenService()
        token = token_service.generate(user=user)
        return Response(data={"data": token}, status=status.HTTP_201_CREATED)


        # validated_data = self.validate(data)

        # otp = validated_data.pop("otp")
        # phone_number = validated_data.get("phone_number")
        # handler = self.handler(self.view, self.request)

        # OTP.objects.verify(phone_number=phone_number, code=otp)
        # user = handler.create(validated_data)
        # User.objects.filter(id=user.id).update(is_verified=True)

        # token_service = TokenService()
        # token = token_service.generate(user=user)
        # return Response(data={"data": token}, status=status.HTTP_201_CREATED)

    def get_by_email(self, data):

        validated_data = self.validate(data)

        email = validated_data.get("email")
        handler = self.handler(self.view, self.request)
        user = handler.get(email=email)
        # self._check_user_ban(user)

        serializer = self.view.get_output_serializer(user)

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


    def get_by_email_or_none(self, data):

        validated_data = self.validate(data)

        email = validated_data.get("email")
        handler = self.handler(self.view, self.request)
        user = handler.get_or_none(email=email)

        if user:
            # self._check_user_ban(user)
            serializer = self.view.get_output_serializer(user)
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

        return Response(data={"data": None}, status=status.HTTP_200_OK)


    # def reset_password(self, data):

    #     validated_data = self.validate(data)

    #     phone_number = validated_data.get("phone_number")
    #     otp = validated_data.get("otp")
    #     password = validated_data.get("password")
    #     handler = self.handler(self.view, self.request)

    #     OTP.objects.verify(phone_number=phone_number, code=otp)
    #     user = handler.get(phone_number=phone_number)

    #     user.set_password(password)
    #     user.save(update_fields=["password"])

    #     return Response(
    #         data={"message": "password changed successfully!"},
    #         status=status.HTTP_204_NO_CONTENT,
    #     )

    # def change_password(self, data):

    #     validated_data = self.validate(data)

    #     handler = self.handler(self.view, self.request)
    #     user_id = self.request.user.id
    #     password = validated_data.get("password")
    #     old_password = validated_data.get("old_password")

    #     user = handler.get(pk=user_id)

    #     if password == old_password:
    #         raise ValidationException(message="The new password cannot be the same as the old password.")

    #     if not user.check_password(old_password):
    #         raise ValidationException(message="Old Password is incorrect")

    #     user.set_password(password)
    #     user.save(update_fields=["password"])

    #     return Response(
    #         data={"message": "password changed successfully!"},
    #         status=status.HTTP_204_NO_CONTENT,
    #     )

    def generate_otp(self, data):

        validated_data = self.validate(data)
        email = validated_data.get("email")
        template = validated_data.get("template")

        if template == EmailTemplates.OTPRegister and User.objects.filter(email=email).exists():
            raise ValidationException(message="User already registered, please sign in")

        mail_service = MailService()

        otp, created = OTP.objects.get_or_create(email=email)
        mail_service.send_otp_email(to=email, otp=otp.code)
        return Response(data={"data": {"status": "sent"}}, status=status.HTTP_200_OK)

    def verify_OTP(self, data):

        validated_data = self.validate(data)

        otp = validated_data.pop("otp")
        email = validated_data.get("email")

        OTP.objects.verify(email=email, code=otp)
        return Response(data={"data": True}, status=status.HTTP_200_OK)
