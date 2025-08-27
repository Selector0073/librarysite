from rest_framework import serializers
from .models import users
from books.models import apikey



class useraddSerializer(serializers.ModelSerializer):

    class Meta:
        model = users
        fields = [
            'username', 'email', 'password'
        ]
    
    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username cant be empty.")
        if users.objects.filter(username=value).exists():
            raise serializers.ValidationError("Account with this username already exists.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("username cant be empty.")
        if users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Account with this email already exists.")
        return value
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cant be empty.")
        return value



class usercheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = [
            'username', 'email', 'password'
        ]



class apiSerializer(serializers.ModelSerializer):
    apikey = serializers.CharField(write_only=True)

    class Meta:
        model = apikey
        fields = [
            'apikey'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apikey'] = serializers.CharField(write_only=True)

    def validate_apikey(self, value):
        if not apikey.objects.filter(apikey=value).exists():
            raise serializers.ValidationError("API key is wrong.")
        return value