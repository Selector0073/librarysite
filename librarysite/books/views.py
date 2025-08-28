from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import books
from .serializers import booksaddSerializer, cardSerializer, ganresSerializer, titleSerializer, redactSerializer



class booksadd(generics.ListAPIView):
    def post(self, request):
        serializer = booksaddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class bookslist(generics.ListAPIView):
    def get(self, request):
        lst = books.objects.all().values()
        return Response({'posts': list(lst)})
    
    
    
class bookscard(generics.ListAPIView):
    def get(self, request):
        serializer = cardSerializer(data=request.data)
        book = books.objects.all() 
        serializer = cardSerializer(book, many=True)
        return Response(serializer.data)
    


class bookscardganres(generics.ListAPIView):
    def get(self, request):
        serializer = ganresSerializer(data=request.data)
        ganre_id = request.data.get('ganres')
        if ganre_id is not None:
            books_qs = books.objects.filter(ganres=ganre_id)
            serializer = ganresSerializer(books_qs, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "ganres parameter is required"}, status=status.HTTP_400_BAD_REQUEST)



class booksdelete(generics.ListAPIView):
    def delete(self, request):
        try:
            upc_qs = request.data.get('upc')
            book = books.objects.get(upc=upc_qs)
            book.delete()
            return Response({"message": f"Book with UPC {upc_qs} deleted successfully."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"Book with UPC {upc_qs} not found."}, status=status.HTTP_404_NOT_FOUND)
        
    


class bookstitle(generics.ListAPIView):
    def get(self, request):
        title_qs = request.data.get('title')
        if title_qs is not None:
            books_qs = books.objects.filter(title=title_qs)
            serializer = titleSerializer(books_qs, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Title parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    


class booksredact(generics.ListAPIView):
    def put(self, request):
        upc = request.data.get('upc')
        if not upc:
            return Response({"error": "UPC is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = books.objects.get(upc=upc)
        except books.DoesNotExist:
            return Response({"error": "Book with this UPC not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = redactSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        