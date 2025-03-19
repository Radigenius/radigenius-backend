from typing import Dict
from uuid import UUID

from rest_framework.response import Response
from rest_framework import status
from application.interfaces.commands.base import IBaseCommand
from infrastructure.exceptions.exceptions import ValidationException
from infrastructure.handlers.base import BaseHandler


class BaseCommand(IBaseCommand):
    def __init__(self, view, request):

        if not self.handler or not issubclass(self.handler, BaseHandler):
            raise NotImplementedError(
                "BaseCommand must have a handler attribute and it must be a subclass of "
                "BaseHandler"
            )

        if not view:
            raise NotImplementedError("BaseCommand must have a view attribute")

        if not request:
            raise NotImplementedError("BaseCommand must have a request attribute")

        self.view = view
        self.request = request

    def _filter_queryset(self, queryset):
        return self.view.filter_queryset(queryset)

    def _paginate_queryset(self, queryset):
        return self.view.paginate_queryset(queryset)

    def _prepare_handler(self):
        return self.handler(self.view, self.request)

    def validate(self, data, *args, **kwargs):

        serializer = self.view.get_input_serializer(data=data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if not bool(validated_data):
            raise ValidationException(message="Empty Payload")

        return validated_data

    def list(self, paginated=False):
        queryset = self._prepare_handler().fetch_list()
        queryset = self._filter_queryset(queryset)

        if paginated:
            page = self._paginate_queryset(queryset)
            if page is not None:
                serializer = self.view.get_output_serializer(page, many=True)
                return self.view.get_paginated_response(serializer.data)

        serializer = self.view.get_output_serializer(queryset, many=True)

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, data: Dict):
        validated_data = self.validate(data)
        queryset = self._prepare_handler().create(validated_data)
        serializer = self.view.get_output_serializer(queryset)

        return Response(data={"data": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, *args, **kwargs):
        queryset = self._prepare_handler().fetch_detail(*args, **kwargs)
        serializer = self.view.get_output_serializer(queryset)

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, pk: UUID, data: Dict):
        data.setdefault("id", pk)
        validated_data = self.validate(data, partial=True)
        queryset = self._prepare_handler().update(pk, validated_data)
        serializer = self.view.get_output_serializer(queryset)

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def partial_update(self, pk: UUID, data: dict):
        data.setdefault("id", pk)
        validated_data = self.validate(data, partial=True)
        queryset = self._prepare_handler().partial_update(pk=pk, data=validated_data)
        serializer = self.view.get_output_serializer(queryset)

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, pk):
        response = self._prepare_handler().delete(pk=pk)
        return Response(data={"data": response}, status=status.HTTP_204_NO_CONTENT)

    def get_list_for_current_user(self, paginated=False):
        queryset = self._prepare_handler().get_list_for_current_user()
        queryset = self._filter_queryset(queryset)

        if paginated:
            page = self._paginate_queryset(queryset)
            if page is not None:
                serializer = self.view.get_output_serializer(page, many=True)
                return self.view.get_paginated_response(serializer.data)

        serializer = self.view.get_output_serializer(queryset, many=True)

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
