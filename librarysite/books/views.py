from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import Book
from .serializers import BookCreateSerializer, BookSerializer, BookDetailsSerializer
from common.permissions import IsAdmin, IsLogged

from .scrape import scrape
from .services import exportbooksexcel


#* done | not tested
class BookCRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLogged]
    queryset = Book.objects.all()
    serializer_class = BookDetailsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title=title)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        title = request.data.get("title")
        book = generics.get_object_or_404(Book, title=title)
        serializer = BookDetailsSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        title = request.data.get("title")
        book = generics.get_object_or_404(Book, title=title)
        book.delete()
        return Response({"message": f"Book '{title}' deleted successfully."}, status=status.HTTP_200_OK)


#* done | not tested
class BookPreviewView(generics.ListAPIView):
    permission_classes = [IsLogged]
    serializer_class = BookSerializer

    def get(self):
        queryset = Book.objects.all()
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        return queryset


#* done
class BooksImportView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    def post(self):
        try:
            scrape()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#* done | not tested
class ExportBooksExcelView(APIView):
    permission_classes = [IsLogged]

    def post(self, request):
        serializer = BookDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        books = Book.objects.all()

        response = exportbooksexcel(books)
        return response


