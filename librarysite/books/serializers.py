from rest_framework import serializers
from .models import books, category



class booksaddSerializer(serializers.ModelSerializer):
    ganres = serializers.PrimaryKeyRelatedField(queryset=category.objects.all())

    class Meta:
        model = books
        fields = [
            'title', 'img', 'reviews', 'content', 'upc', 'producttype',
            'price', 'pricetax', 'tax', 'availability', 'reviewscount', 'ganres', 'date'
        ]
    
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cant be empty.")
        if books.objects.filter(title=value).exists():
            raise serializers.ValidationError("Book with this title already exists.")
        return value

    def validate_img(self, value):
        if not value:
            raise serializers.ValidationError("Img cant be empty.")
        return value

    def validate_reviews(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Reviews cant be negative.")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content cant be empty.")
        return value

    def validate_upc(self, value):
        if not value:
            raise serializers.ValidationError("UPC cant be empty.")
        if books.objects.filter(upc=value).exists():
            raise serializers.ValidationError("Book with this UPC already exists.")
        return value

    def validate_producttype(self, value):
        if not value:
            raise serializers.ValidationError("Product type cant be empty.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cant be negative.")
        return value

    def validate_pricetax(self, value):
        if value < 0:
            raise serializers.ValidationError("Pricetax cant be negative.")
        return value

    def validate_tax(self, value):
        if value < 0:
            raise serializers.ValidationError("Tax cant be negative.")
        return value

    def validate_availability(self, value):
        if value < 0:
            raise serializers.ValidationError("Availability cant be negative.")
        return value

    def validate_reviewscount(self, value):
        if value < 0:
            raise serializers.ValidationError("Reviewscount cant be negative.")
        return value

    def validate_ganres(self, value):
        if not (1 <= value.id <= 51):
            raise serializers.ValidationError("Ganres must be from 1 to 51.")
        return value
    
    def validate_content(self, value):
        my_date = serializers.DateField(
            input_formats=['%Y-%m-%d'],
            error_messages={'invalid': 'Date must be in this format YYYY-MM-DD'}
        )
        return value
    


class cardSerializer(serializers.ModelSerializer):
    class Meta:
        model = books
        fields = [
            'title', 'img', 'reviews', 'availability', 'pricetax'
        ]



class ganresSerializer(serializers.ModelSerializer):
    class Meta:
        model = books
        fields = [
            'title', 'img', 'reviews', 'availability', 'pricetax'
        ]



class titleSerializer(serializers.ModelSerializer):
    class Meta:
        model = books
        fields = [
            'title', 'img', 'reviews', 'content', 'upc', 'producttype',
            'price', 'pricetax', 'tax', 'availability', 'reviewscount', 'ganres', 'date'
        ]



class redactSerializer(serializers.ModelSerializer):
    upc = serializers.CharField(read_only=True)
    ganres = serializers.PrimaryKeyRelatedField(queryset=category.objects.all())

    class Meta:
        model = books
        fields = [
            'title', 'img', 'reviews', 'content', 'upc', 'producttype',
            'price', 'pricetax', 'tax', 'availability', 'reviewscount', 'ganres', 'date'
        ]


    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cant be empty.")
        if books.objects.filter(title=value).exists():
            raise serializers.ValidationError("Book with this title already exists.")
        return value

    def validate_img(self, value):
        if not value:
            raise serializers.ValidationError("Img cant be empty.")
        return value

    def validate_reviews(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Reviews cant be negative.")
        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("Content cant be empty.")
        return value

    def validate_producttype(self, value):
        if not value:
            raise serializers.ValidationError("Product type cant be empty.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cant be negative.")
        return value

    def validate_pricetax(self, value):
        if value < 0:
            raise serializers.ValidationError("Pricetax cant be negative.")
        return value

    def validate_tax(self, value):
        if value < 0:
            raise serializers.ValidationError("Tax cant be negative.")
        return value

    def validate_availability(self, value):
        if value < 0:
            raise serializers.ValidationError("Availability cant be negative.")
        return value

    def validate_reviewscount(self, value):
        if value < 0:
            raise serializers.ValidationError("Reviewscount cant be negative.")
        return value

    def validate_ganres(self, value):
        if not (1 <= value.id <= 51):
            raise serializers.ValidationError("Ganres must be from 1 to 51.")
        return value
    
    def validate_content(self, value):
        my_date = serializers.DateField(
            input_formats=['%Y-%m-%d'],
            error_messages={'invalid': 'Date must be in this format YYYY-MM-DD'}
        )
        return value