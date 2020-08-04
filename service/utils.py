from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    exc_response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if exc_response is not None:
        exc_response.data['errors'] = exc_response.status_text
        exc_response.data['data'] = None

    return exc_response


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
    headers = kwargs.get('headers', None)

    return Response(data=response_data, status=response_status, headers=headers)
