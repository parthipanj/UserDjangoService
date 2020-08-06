import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from service import constants
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
        logging.info('type=%s msg=%s' % (constants.USER_CREATE_API_INIT, 'user create API initiated'))

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            logging.info('type=%s msg=%s' % (constants.USER_CREATE_API_SUCCESS, 'User created successfully'))

            headers = self.get_success_headers(serializer.data)
            return response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        logging.error('type=%s msg=%s' % (constants.USER_CREATE_API_ERROR, 'Validation error in user create request'))
        return response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List a user queryset.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logging.info('type=%s msg=%s' % (constants.USER_LIST_API_INIT, 'User list API initiated'))

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            logging.debug('type=%s msg=%s' % (constants.USER_LIST_API_WITH_PAGINATION, 'User list with pagination'))

            serializer = self.get_serializer(page, many=True)
            page_data = self.get_paginated_response(serializer.data)

            logging.info('type=%s msg=%s' % (constants.USER_LIST_API_SUCCESS, 'User list fetched successfully'))
            return response(data=page_data.data)

        logging.debug('type=%s msg=%s' % (constants.USER_LIST_API_WITHOUT_PAGINATION, 'User list without pagination'))
        serializer = self.get_serializer(queryset, many=True)

        logging.info('type=%s msg=%s' % (constants.USER_LIST_API_SUCCESS, 'User list fetched successfully'))
        return response(data=serializer.data)

    def get_object(self):
        """
        Retrieve a user model instance.
        :return:
        """
        try:
            return User.objects.get(pk=self.kwargs.get(self.lookup_field))
        except User.DoesNotExist:
            logging.error('type=%s msg=%s' % (constants.USER_NOT_FOUND, 'User does not exist'))
            raise NotFound(_('User does not exist'))

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logging.info('type=%s msg=%s' % (constants.USER_RETRIEVE_API_INIT, 'User retrieve API initiated'))

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        logging.info('type=%s msg=%s' % (constants.USER_RETRIEVE_API_SUCCESS, 'User detail retrieved successfully'))
        return response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logging.info('type=%s msg=%s' % (constants.USER_UPDATE_API_INIT, 'User update API initiated'))

        partial = kwargs.pop('partial', False)

        logging.debug('type=%s msg=%s data=%s' % (
            constants.USER_UPDATE_API_IS_PARTIAL, 'User request is for with or without partial update',
            {'is_partial': partial}))

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            self.perform_update(serializer)

            logging.info('type=%s msg=%s' % (constants.USER_UPDATE_API_SUCCESS, 'User updated successfully'))
            return response(data=serializer.data)

        logging.error('type=%s msg=%s' % (constants.USER_UPDATE_API_ERROR, 'Validation error in user update request'))
        return response(errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial update a user model instance.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        logging.info('type=%s msg=%s' % (constants.USER_PARTIAL_UPDATE_API_INIT, 'User partial update API initiated'))

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
        logging.info('type=%s msg=%s' % (constants.USER_DESTROY_API_INIT, 'User destroy API initiated'))

        instance = self.get_object()
        self.perform_destroy(instance)

        logging.info('type=%s msg=%s' % (constants.USER_DESTROY_API_SUCCESS, 'User deleted successfully'))
        return Response(status=status.HTTP_204_NO_CONTENT)
