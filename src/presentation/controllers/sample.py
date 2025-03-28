from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.http import StreamingHttpResponse

from domain.apps.conversation.models import Message

from infrastructure.services.inference import InferenceService
class SampleViewSet(ViewSet):
    def retrieve(self, request):
        inference_service = InferenceService()
        message = Message.objects.get_or_not_found_exception(id="a492acab-7201-496c-95d2-abf82875f126")
        response = inference_service.send_message(message, [])
        

        # Start streaming response
        def stream_response():
            for chunk in response:
                yield f"data: {chunk}\n\n"
        
        return StreamingHttpResponse(
            streaming_content=stream_response(),
            content_type='text/event-stream'
        )

        # return Response(data=response, status=200)
