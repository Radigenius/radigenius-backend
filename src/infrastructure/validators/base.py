from typing import Dict, List
from cerberus import Validator as CerberusValidator
from cerberus.errors import BasicErrorHandler
from rest_framework.serializers import Serializer

from infrastructure.exceptions.exceptions import ValidationException


class CustomErrorHandler(BasicErrorHandler):
    pass


Validator = CerberusValidator(allow_unknown=True, error_handler=CustomErrorHandler)


class BaseSerializerValidator:
    requires_context = True

    def __init__(self, field_name):
        self.field_name = field_name

    def _collect_errors(self, data: Dict, serializer: Serializer) -> List[str]:
        return []

    def __call__(self, data, serializer: Serializer):

        partial = serializer.partial
        serializer_field = serializer.fields.get(self.field_name)
        read_only, required = (
            serializer_field.read_only,
            serializer_field.required,
        )
        value = data.get(self.field_name, None)

        if read_only and value is not None:
            raise ValidationException(
                errors=[{f"{self.field_name}": ["This Field Is ReadOnly"]}]
            )

        if not partial and required and value is None:
            raise ValidationException(
                errors=[
                    {f"{self.field_name}": [serializer.error_messages.get("required")]}
                ]
            )

        errors = []

        if value:
            errors = self._collect_errors(data, serializer)

        if len(errors) > 0:
            raise ValidationException(errors={f"{self.field_name}": errors})
