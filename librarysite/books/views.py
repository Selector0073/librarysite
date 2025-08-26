from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import books
from .serializers import booksSerializer

#from .models import category

class booksAPIView(generics.ListAPIView):
    queryset = books.objects.all()
    serializer_class = booksSerializer

#    def get(self, request):
#        lst = books.objects.all().values()
#        return Response({'posts': list(lst)})
#
#    def post(self, request):
#        category_instance = category.objects.get(id=request.data['ganres'])
#        post_new = books.objects.create(
#            title=request.data['title'],
#            img=request.data['img'],
#            reviews=request.data['reviews'],
#            content=request.data['content'],
#            upc=request.data['upc'],
#            producttype=request.data['producttype'],
#            price=request.data['price'],
#            pricetax=request.data['pricetax'],
#            tax=request.data['tax'],
#            availability=request.data['availability'],
#            reviewscount=request.data['reviewscount'],
#            ganres=category_instance
#        )
#
#        return Response({'post': model_to_dict(post_new)})
#
#        
#        # return Response({'title': 'postt'})