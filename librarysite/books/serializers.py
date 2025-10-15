from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Book, Category



class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'writed_at', 'author'
        ]



class BookSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'img', 'reviews', 'availability', 'price'
        ]



class BookDetailsSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    id = serializers.ReadOnlyField()
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'writed_at', 'author'
        ]


