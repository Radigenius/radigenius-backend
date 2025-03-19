from rest_framework.serializers import (
    Serializer,
    EmailField,
)

class EmailSerializer(Serializer):
    email = EmailField(max_length=None, min_length=None, allow_blank=False)