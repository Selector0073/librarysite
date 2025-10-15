from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from rest_framework import status

from .serializers import UserSerializer
import os
import string
import secrets


def generate_password(length=20):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def reset_password(request_data):
    User = get_user_model()
    load_dotenv()
    serializer = UserSerializer(data=request_data)
    if not serializer.is_valid():
        return {"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST}

    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")

    try:
        user = User.objects.get(username=username, email=email)
    except User.DoesNotExist:
        return {"data": {"error": "User not found"}, "status": status.HTTP_404_NOT_FOUND}

    new_password = generate_password()
    user.set_password(new_password)
    user.password_need_reset = True
    user.save()

    send_mail(
        subject="Password Reset - Library",
        message=f"Your new password: {new_password}",
        from_email=os.getenv("EMAIL"),
        recipient_list=[email],
        fail_silently=False,
    )

    return {"data": {"message": "Password reset email sent"}, "status": status.HTTP_200_OK}
