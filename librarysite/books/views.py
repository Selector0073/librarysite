from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import Book
from .serializers import BookCreateSerializer, BookSerializer, BookDetailsSerializer
from common.permissions import IsAdmin, IsLogged
from .scrape import scrape
import openpyxl
from django.http import HttpResponse



class BookCRUDView(generics.ListAPIView):
    permission_classes = [IsLogged]
    #*All books | Filter by title/genre
    def get(self, request):    
        genre_qs = request.data.get('genre')
        title_qs = request.data.get('title')

        if genre_qs is not None and title_qs is None:
            queryset = Book.objects.filter(genre=genre_qs)
            serializer = BookSerializer(queryset, many=True)
            return Response(serializer.data)

        elif genre_qs is None and title_qs is not None:
            queryset = Book.objects.filter(title=title_qs)
            serializer_class = BookDetailsSerializer(queryset, many=True)
            return Response(serializer_class.data)

        elif genre_qs is None and title_qs is None:
            serializer_class = BookDetailsSerializer(many=True)
            return Response(serializer_class.data)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    #*Delete
    def delete(self, request):
        try:
            title_qs = request.data.get('title')
            book = Book.objects.get(title=title_qs)
            book.delete()
            return Response({"message": f"Book with title {title_qs} deleted successfully."}, status=status.HTTP_200_OK)
        except:
            return Response({"error": f"Book with title {title_qs} not found."}, status=status.HTTP_404_NOT_FOUND)


    #*Create
    def post(self, request):
        serializer_class = BookCreateSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


    #*RedactBook
    def put(self, request):
        serializer = BookDetailsSerializer(
            data=request.data, 
            partial=True,
            context={"mode": "RedactBook"}
        )
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookDetailsSerializer(book).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookPreviewView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        serializer_class = BookSerializer(data=request.data)
        book = Book.objects.all() 
        serializer_class = BookSerializer(book, many=True)
        return Response(serializer_class.data)



class BooksImportView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        try:
            scrape()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ExportBooksExcelView(APIView):
    permission_classes = [IsLogged]
    def post(self, request):
        serializer_class = BookDetailsSerializer(
            data=request.data,
            context={"mode": "ExportBooksExcel"}
        )

        if not serializer_class.is_valid():
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        books = serializer_class.GetData()

        excel = openpyxl.Workbook()
        sheet = excel.active
        sheet.title = "Books"

        sheet.append([
            'title', 'img', 'reviews', 'content',
            'price', 'availability', 'reviews_count',
            'genre', 'writed_at', 'author'
        ])

        for book in books:
            sheet.append([
                book.title,
                book.img,
                book.reviews,
                book.content,
                book.price,
                book.availability,
                book.reviews_count,
                str(book.genre),
                book.writed_at.isoformat(),
                book.author
            ])

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="books.xlsx"'
        excel.save(response)
        return response
