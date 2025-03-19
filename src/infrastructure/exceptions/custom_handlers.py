from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError

from infrastructure.exceptions.exceptions import BaseCustomException
from sentry_sdk import capture_exception, capture_message


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Handle ValidationError of DRF
    # fixing the response format of DRF
    if isinstance(exc, ValidationError):
        response.data['key'] = "validation_error"
        code = status.HTTP_400_BAD_REQUEST

    if response is not None and isinstance(exc, BaseCustomException):
        response.data["errors"] = exc.errors
        response.data["key"] = exc.key
        code  = exc.status_code

    # Handle Python exceptions
    elif isinstance(exc, Exception) and not isinstance(exc, APIException):
        response = Response(data={"errors": exc.args, "message": "Internal Server Error!", "key": "internal_server_error"}, status=code)

    if status.is_server_error(code):
        capture_exception(exc)
    elif status.is_client_error(code):
        capture_message(exc)

    return response
