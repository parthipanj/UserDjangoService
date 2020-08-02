from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
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
