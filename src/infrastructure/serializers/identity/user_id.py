from rest_framework.serializers import Serializer, CharField

class UserIdSerializer(Serializer):
    user_id = CharField(required=True)