from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer
from common.permissions import IsLogged

from .services import reset_password
from dotenv import load_dotenv



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


#*done | not tested
class UserEmailSendView(APIView):
    def post(self, request):
        result = reset_password(request.data)
        return Response(result["data"], status=result["status"])



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
