from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Book, Category



class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'writed_at', 'author'
        ]
        
        def validate_title(self, value):
            if Book.objects.filter(title=value).exists():
                raise serializers.ValidationError("Book with this title already exists.")
            return value



class Book(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'availability', 'price'
        ]



class BookDetails(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'writed_at', 'author'
        ]



class BookRedactSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(read_only=True)
    genre = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'writed_at', 'author'
        ]
