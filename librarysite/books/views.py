from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from .models import Book
from .serializers import BookCreateSerializer, BookSerializer, BookDetailsSerializer
from common.permissions import IsAdmin, IsLogged

from datetime import datetime
from .scrape import scrape
from .services import exportbooksexcel



#* done
class BookCRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLogged]
    queryset = Book.objects.all()
    serializer_class = BookDetailsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(id=id)
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
        id = request.data.get("id")
        book = generics.get_object_or_404(Book, id=id)
        serializer = BookDetailsSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = request.data.get("id")
        book = generics.get_object_or_404(Book, id=id)
        book.delete()
        return Response({"message": f"Book '{id}' deleted successfully."}, status=status.HTTP_200_OK)



#* done
class BookSearchPreviewView(generics.ListAPIView):
    permission_classes = [IsLogged]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = Book.objects.all()
        genre_name = self.request.query_params.get('genre')
        if genre_name:
            queryset = queryset.filter(genre__genre__iexact=genre_name)
        date_str = self.request.query_params.get('writed_at')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(writed_at__gte=date_obj)
            except ValueError:
                pass
        return queryset



#* done
class BooksImportView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    def post(self):
        try:
            scrape()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#* done
class ExportBooksExcelView(APIView):
    permission_classes = [IsLogged]

    def post(self, request):
        serializer = BookDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        books = Book.objects.all()

        response = exportbooksexcel(books)
        return response


