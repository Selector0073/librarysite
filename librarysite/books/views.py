from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Book
from .serializers import BookCreateSerializer, BookPreviewShowSerializer, BookGengesFilterShowSerializer, BookShowByTitleSerializer, BookRedactSerializer
from common.permissions import IsAdmin, IsLogged
import subprocess
import os
import openpyxl
from django.http import HttpResponse



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



class BooksImportView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        try:
            script_path = os.path.join(os.path.dirname(__file__), "scrape.py")
            subprocess.run(["python", script_path])
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ExportBooksExcelView(generics.ListAPIView):
    permission_classes = [IsLogged]
    def get(self, request):
        genre_qs = request.data.get('genre')
        title_qs = request.data.get('title')

        excel = openpyxl.Workbook()
        sheet = excel.active
        sheet.title = "Books"

        sheet.append([
            'title', 'img', 'reviews', 'content',
            'price', 'availability', 'reviews_count',
            'genre', 'date'
        ])

        if genre_qs == None and title_qs == None:
            for book in Book.objects.all():
                sheet.append([
                    book.title,
                    book.img,
                    book.reviews,
                    book.content,
                    book.price,
                    book.availability,
                    book.reviews_count,
                    str(book.genre),
                    book.date.isoformat()
                ])

            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = 'attachment; filename="books.xlsx"'
            excel.save(response)
            return response
        elif genre_qs != None and title_qs == None:
            books = Book.objects.filter(genre=genre_qs)
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
                    book.date.isoformat()
                ])

            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = 'attachment; filename="books.xlsx"'
            excel.save(response)
            return response
        
        elif title_qs != None and genre_qs == None:
            books = Book.objects.filter(title=title_qs)
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
                    book.date.isoformat()
                ])

            response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = 'attachment; filename="books.xlsx"'
            excel.save(response)
            return response
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

