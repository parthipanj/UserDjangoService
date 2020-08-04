from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from service.utils import response
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a user instance.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        """
        Create a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List a user queryset.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            page_data = self.get_paginated_response(serializer.data)
            return response(data=page_data.data)

        serializer = self.get_serializer(queryset, many=True)
        return response(data=serializer.data)

    def get_object(self):
        """
        Retrieve a user model instance.
        :return:
        """
        try:
            return User.objects.get(pk=self.kwargs.get(self.lookup_field))
        except User.DoesNotExist:
            raise NotFound(_('User does not exist'))

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            self.perform_update(serializer)
            return response(data=serializer.data)

        return response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial update a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
