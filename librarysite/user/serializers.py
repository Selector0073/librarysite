from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User



class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'is_admin'
        ]
