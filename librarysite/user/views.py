from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import User
from .serializers import UserCreateSerializer, UserCheckSerializer
from common.permissions import IsAdmin


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
    def get(self, request):
        queryset = request.data.get('username')
        if queryset is not None:
            queryset = User.objects.filter(username=queryset)
            serializer_class = UserCheckSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            return Response({"error": "Username parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
