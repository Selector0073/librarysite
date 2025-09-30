from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mode = self.context.get("mode")

        if mode == "ChangePassword":
            self.fields['username'].validators = [
                v for v in self.fields['username'].validators 
                if not isinstance(v, UniqueValidator)
            ]
            self.fields["username"].required = True
            self.fields["email"].required = False
            self.fields["password"].required = True

        elif mode == "UserCreate":
            self.fields["username"].required = True
            self.fields["email"].required = True
            self.fields["password"].required = True

        elif mode == "UserResetPassword":
            self.fields['username'].validators = [
                v for v in self.fields['username'].validators 
                if not isinstance(v, UniqueValidator)
            ]
            self.fields['email'].validators = [
                v for v in self.fields['email'].validators 
                if not isinstance(v, UniqueValidator)
            ]
            self.fields["username"].required = True
            self.fields["email"].required = True
            self.fields["password"].required = False

    def validate_username(self, value):
        mode = self.context.get("mode")
        if mode == "ChangePassword" or mode == "UserResetPassword":
            if not User.objects.filter(username=value).exists():
                raise serializers.ValidationError("No user with this username")
            else:
                user = User.objects.get(username=value)
                self.instance = user
        return value

    def validate_email(self, value):
        mode = self.context.get("mode")
        if mode == "UserResetPassword":
            if not User.objects.filter(email=value).exists():
                raise serializers.ValidationError("No user with this email")
            else:
                user = User.objects.get(email=value)
                self.instance = user
        return value
    
    def update(self, instance, validated_data):
        self.instance.set_password(validated_data["password"])
        self.instance.save()
        return self.instance

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_admin=validated_data.get('is_admin', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
