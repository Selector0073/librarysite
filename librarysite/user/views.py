from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import User
from .serializers import UserCreateSerializer, UserCheckSerializer
from common.permissions import IsLogged
import smtplib
import random
import string




from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


# Create user
class UserCreateView(generics.CreateAPIView):
    def post(self, request):
        serializer_class = UserCreateSerializer(data=request.data)
        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=request.data.get('username'),
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)


# Check user information
class UserCheckView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        queryset = request.data.get('username')
        if queryset is not None:
            queryset = User.objects.filter(username=queryset)
            serializer_class = UserCheckSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            return Response({"error": "Username parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


# Email to reset password
class UserEmailSendView(generics.ListAPIView):
    def post(self, request):
        username = request.data.get('username')
        user_email = request.data.get('email')
        if not username or not user_email:
            return Response({"error": "Username and email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            username = User.objects.get(username=username)
            email = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"error": "Account with this email and username are not exist"}, status=status.HTTP_404_NOT_FOUND)

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        username.set_password(new_password)
        username.save()

        email_sender = "YOUR_EMAIL_HERE"
        subject = "Reset password for library site"
        message = "Your new password is: " + new_password
        text = f"Subject: {subject}\n\n{message}"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_sender, "YOUR_APP_PASSWORD_IS_HERE")
        server.sendmail(email_sender, user_email, text)

        return Response({"email": "succesfuly sended"}, status=status.HTTP_200_OK)





# TODO: ADD CHENGE PASSWORD BUTTON
