from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


def response(**kwargs):
    """
    Custom response
    :param kwargs:
    :return:
    """
    response_data = {
        'data': kwargs.get('data', None),
        'errors': kwargs.get('errors', None)
    }

    response_status = kwargs.get('status', status.HTTP_200_OK)

    return Response(data=response_data, status=response_status)


class UserViewSet(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a user instance.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        """
        Create a model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return response(data=serializer.data, status=status.HTTP_201_CREATED)

        return response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List a user queryset.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = User.objects.all()

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
        return response(data=serializer.data)

    def get_object(self, pk):
        """
        Retrieve a user model instance.
        :param pk:
        :return:
        """
        try:
            return User.objects.get(pk=pk)
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
        instance = self.get_object(kwargs.get('pk'))
        serializer = UserSerializer(instance)
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
        instance = self.get_object(kwargs.get('pk'))

        serializer = UserSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
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
        instance = self.get_object(kwargs.get('pk'))
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
