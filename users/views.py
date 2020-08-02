from django.contrib.auth.hashers import make_password
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data.get('password')))
