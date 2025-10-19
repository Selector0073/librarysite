from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer
from common.permissions import IsLogged, CanChangePassword

from .services import reset_password



#*done | not tested
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()



#*done | not tested
class UserCheckView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsLogged]

    def get_queryset(self):
        id = self.request.query_params.get("id")
        if id:
            return User.objects.filter(id=id)
        return User.objects.none()



#*done | not tested
class UserEmailSendView(APIView):
    def post(self, request):
        result = reset_password(request.data)
        return Response(result["data"], status=result["status"])



#*done | not tested
class UserPasswordChangeView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [CanChangePassword]
    allow_password_change_for_reset = True

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(User, 'password_need_reset', False):
            User.password_need_reset = False
            User.save(update_fields=['password_need_reset'])

