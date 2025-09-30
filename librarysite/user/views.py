from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer
from common.permissions import IsLogged
import smtplib
import random
import string
from dotenv import load_dotenv
import os


# Create user
class UserCreateView(generics.CreateAPIView):
    def post(self, request):
        serializer_class = UserSerializer(
            data=request.data,
            context={"mode": "UserCreate"}
        )

        if serializer_class.is_valid():
            serializer_class.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



# Check user information
class UserCheckView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        queryset = request.data.get('username')
        if queryset is not None:
            queryset = User.objects.filter(username=queryset)
            serializer_class = UserSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            return Response({"error": "Username parameter is required"}, status=status.HTTP_400_BAD_REQUEST)



# Email to reset password
class UserEmailSendView(APIView):
    def post(self, request):
        load_dotenv()
        serializer_class = UserSerializer(
            data=request.data,
            context={"mode": "UserResetPassword"}
        )
        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_email = serializer_class.validated_data.get('email')
        username = User.objects.get(username=serializer_class.validated_data.get('username'))

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        username.set_password(new_password)
        username.save()

        email_sender = os.getenv("EMAIL")
        subject = "Reset password for library site"
        message = "Your new password is: " + new_password
        text = f"Subject: {subject}\n\n{message}"
        server = smtplib.SMTP(os.getenv('SERVICE'), 587)
        server.starttls()
        server.login(email_sender, os.getenv('APP_PASSWORD'))
        server.sendmail(email_sender, user_email, text)

        return Response({"email": "succesfuly sended"}, status=status.HTTP_200_OK)



# Change password
class UserPasswordChangeView(APIView):
    permission_classes = [IsLogged]
    def put(self, request):
        serializer_class = UserSerializer(
            data=request.data,
            context={"mode": "ChangePassword"}
        )
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
