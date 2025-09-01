from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Book
from .serializers import BookCreateSerializer, BookPreviewShowSerializer, BookGengesFilterShowSerializer, BookShowByTitleSerializer, BookRedactSerializer
from common.permissions import IsAdmin, IsLogged


# * GET

class BookListView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        lst = Book.objects.all().values()
        return Response({'Books': list(lst)})



class BookPreviewView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        serializer_class = BookPreviewShowSerializer(data=request.data)
        book = Book.objects.all() 
        serializer_class = BookPreviewShowSerializer(book, many=True)
        return Response(serializer_class.data)



class BookGengesFilterView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        serializer_class = BookGengesFilterShowSerializer(data=request.data)
        ganre_id = request.data.get('genre')
        if ganre_id is not None:
            queryset = Book.objects.filter(ganres=ganre_id)
            serializer_class = BookGengesFilterShowSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            return Response({"error": "Genre parameter is required"}, status=status.HTTP_400_BAD_REQUEST)



class BookShowByTitleView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        queryset = request.data.get('title')
        if queryset is not None:
            queryset = Book.objects.filter(title=queryset)
            serializer_class = BookShowByTitleSerializer(queryset, many=True)
            return Response(serializer_class.data)
        else:
            return Response({"error": "Title parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


# * ELSE

class BookRedactView(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    def put(self, request):
        title = request.data.get('title')
        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(title=title)
        except Book.DoesNotExist:
            return Response({"error": "Book with this title not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer_class = BookRedactSerializer(book, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



class BookCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        serializer_class = BookCreateSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



class BookDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    def delete(self, request):
        try:
            title_qs = request.data.get('title')
            book = Book.objects.get(title=title_qs)
            book.delete()
            return Response({"message": f"Book with title {title_qs} deleted successfully."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"Book with title {title_qs} not found."}, status=status.HTTP_404_NOT_FOUND)


