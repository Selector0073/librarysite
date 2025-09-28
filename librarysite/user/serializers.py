from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'is_admin'
        ]
        extra_kwargs = {
            'is_admin': {'required': False},
            'password': {'write_only': True},
        }
