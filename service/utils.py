from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom Exception Handler
    Call REST framework's default exception handler first to get the standard error response.
    :param exc:
    :param context:
    :return:
    """
    exc_response = exception_handler(exc, context)

    # Now add the errors and data to the response.
    if exc_response is not None:
        return response(errors=exc_response.data, status=exc.status_code)

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
