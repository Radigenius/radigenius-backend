from decouple import config
from django.conf import settings

from rest_framework.serializers import Field, ListSerializer, CharField, Serializer
from infrastructure.exceptions.exceptions import ValidationException


class EnumSerializerField(Field):
    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def get_attribute(self, instance):
        # Return the enum_class directly instead of looking for an attribute in data
        return self.enum_class

    def to_representation(self, value):
        return [
            {"key": choice.label, "value": choice.value} for choice in self.enum_class
        ]

    def to_internal_value(self, data):
        valid_values = [choice.value for choice in self.enum_class]
        if data not in valid_values:
            raise ValidationException(message=f"{data} is not a valid choice.")
        return data


class KeyPairSerializer(Serializer):
    """
    Serializer that allows for dynamic key-value pair naming and data retrieval.
    Supports both single instances and lists when used with many=True.
    """

    def to_representation(self, instance):
        # Retrieve the key and value fields and output names from the context
        key_name = self.context.get("key_name", "code")
        key_field = self.context.get("key_field", "code")
        value_name = self.context.get("value_name", "value")
        value_field = self.context.get("value_field", "value")

        # Serialize a single instance
        return {
            key_name: instance.get(key_field),
            value_name: instance.get(value_field),
        }

    class Meta:
        list_serializer_class = ListSerializer
