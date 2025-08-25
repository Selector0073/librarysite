from rest_framework import serializers
from .models import books

class booksSerializer(serializers.ModelSerializer):
    class Meta: 
        model = books
        fields = ('title', 'img', 'reviews', 'content', 'upc', 'producttype', 'price', 'pricetax', 'tax', 'availability', 'reviewscount', 'ganres')
