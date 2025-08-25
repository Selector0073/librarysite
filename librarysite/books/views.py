from django.shortcuts import render
from rest_framework import generics
from .models import books
from .serializers import booksSerializer

class booksAPIView(generics.ListAPIView):
    queryset = books.objects.all()
    serializer_class = booksSerializer