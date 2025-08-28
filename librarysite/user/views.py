from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import users
from .serializers import useraddSerializer, usercheckSerializer, apiSerializer



class useradd(generics.ListAPIView):
    def post(self, request):
        serializer = useraddSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class usercheck(generics.ListAPIView):
    def get(self, request):
        user_qs = request.data.get('username')
        if user_qs is not None:
            user_qs = users.objects.filter(username=user_qs)
            serializer = usercheckSerializer(user_qs, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Username parameter is required"}, status=status.HTTP_400_BAD_REQUEST)