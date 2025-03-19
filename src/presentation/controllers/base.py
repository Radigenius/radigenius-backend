from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.settings import api_settings

from infrastructure.exceptions.exceptions import (
    NotAuthenticatedException,
    PermissionDeniedException,
)
from infrastructure.responses.responses import (
    BadRequestResponse,
    PermissionDeniedResponse,
    NotFoundResponse,
    ServerErrorResponse,
)


def custom_error_400(request, exception):
    return BadRequestResponse()


def custom_error_403(request, exception):
    return PermissionDeniedResponse()


def custom_error_404(request, exception):
    return NotFoundResponse()


def custom_error_500(request):
    return ServerErrorResponse()


class CustomGenericAPIView(APIView):
    input_serializer_class = None
    output_serializer_class = None

    command_class = None

    # If you want to use object lookups other than pk, set 'lookup_field'.
    # For more complex lookup requirements override `get_object()`.
    lookup_field = "pk"
    lookup_url_kwarg = None

    # The filter backend classes to use for queryset filtering
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    # The style to use for queryset pagination.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticatedException()
        raise PermissionDeniedException()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def set_input_serializer_class(self):
        """This method can be used to customize input serializer on different actions"""
        pass

    def get_input_serializer_class(self):
        """This method is used to get input_serializer_class if is defined at class level"""

        self.set_input_serializer_class()
        return self.input_serializer_class

    def set_output_serializer_class(self):
        """This method can be used to customize output serializer on different actions"""
        pass

    def get_output_serializer_class(self):
        """This method is used to get output_serializer_class if is defined at class level"""

        self.set_output_serializer_class()
        return self.output_serializer_class

    def get_output_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for output response
        """
        serializer_class = self.get_output_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_input_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for input response
        """
        serializer_class = self.get_input_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class CustomGenericViewSet(ViewSetMixin, CustomGenericAPIView):
    pass
