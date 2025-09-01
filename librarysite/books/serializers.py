from rest_framework import serializers
from .models import Book, Category


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'date'
        ]



class BookPreviewShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'availability', 'price'
        ]



class BookGengesFilterShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'availability', 'price'
        ]



class BookShowByTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'date'
        ]



class BookRedactSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    genre = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'date'
        ]

