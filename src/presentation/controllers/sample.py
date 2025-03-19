from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class SampleViewSet(ViewSet):
    def retrieve(self, request):
        return Response(data="Hello World", status=200)
