import re
from typing import List

from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer

from infrastructure.exceptions.exceptions import ValidationException
from infrastructure.validators.base import BaseSerializerValidator

User = get_user_model()

class BaseRegexValidator(BaseSerializerValidator):
    pattern = ""

    def _collect_errors(self, data, serializer: Serializer) -> List[str]:
        errors = super()._collect_errors(data, serializer)
        value = data.get(self.field_name)

        if not re.match(self.pattern, value):
            errors.append("Invalid Format")

        return errors


class PasswordValidator(BaseSerializerValidator):
    """Validate that the password meets all validator requirements."""

    message = "Password is not Valid!"

    def _collect_errors(self, data, serializer: Serializer) -> List[str]:
        errors = super()._collect_errors(data, serializer)
        value = data.get(self.field_name)
        password_validators = get_default_password_validators()

        for validator in password_validators:
            try:
                validator.validate(value, None)
            except ValidationError as error:
                errors.append(error.message)

        return errors


class EitherFieldRequired(BaseSerializerValidator):
    """Either one of the given field is required."""

    message = "Either {} or {} is required"

    def __init__(self, field_name, field2):
        super().__init__(field_name)
        self.field2 = field2

    def __call__(self, data, serializer: Serializer) -> List[str]:
        super().__call__(data, serializer)
        field1 = data.get(self.field_name)
        field2 = data.get(self.field2)

        errors = []

        if not field1 and not field2:
            errors.append(self.message.format(self.field_name, self.field2))

        if len(errors) > 0:
            raise ValidationException(errors=[{f"{self.field_name}": errors}])


class PostalCodeValidator(BaseRegexValidator):
    pattern = r"\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b"
    message = "Postal Code is not Valid!"
