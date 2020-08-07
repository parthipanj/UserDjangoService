from rest_framework import serializers

from service.settings import UPLOADED_FILES_USE_URL
from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=UPLOADED_FILES_USE_URL)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'mobile_number', 'password', 'avatar', 'dob',
            'gender', 'is_active', 'created', 'updated'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'updated': {'read_only': True}
        }
