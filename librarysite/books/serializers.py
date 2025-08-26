from rest_framework import serializers
from .models import books, category, apikey

class booksaddSerializer(serializers.ModelSerializer):
    ganres = serializers.PrimaryKeyRelatedField(queryset=category.objects.all())
    apikey = serializers.CharField(write_only=True)

    class Meta:
        model = books
        fields = [
            'apikey', 'title', 'img', 'reviews', 'content', 'upc', 'producttype',
            'price', 'pricetax', 'tax', 'availability', 'reviewscount', 'ganres'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apikey'] = serializers.CharField(write_only=True)

    def validate_apikey(self, value):
        if not apikey.objects.filter(apikey=value).exists():
            raise serializers.ValidationError("API key is wrong.")
        return value
    
    def create(self, validated_data):
        validated_data.pop('apikey', None)
        return super().create(validated_data)
    
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cant be empty.")
        return value

    def validate_img(self, value):
        if not value:
            raise serializers.ValidationError("Img cant be empty.")
        return value

    def validate_reviews(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Reviews cant be negative.")
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
        if value < 0 or value != 0:
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
    

class apiSerializer(serializers.ModelSerializer):
    apikey = serializers.CharField(write_only=True)

    class Meta:
        model = books
        fields = [
            'apikey'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apikey'] = serializers.CharField(write_only=True)

    def validate_apikey(self, value):
        if not apikey.objects.filter(apikey=value).exists():
            raise serializers.ValidationError("API key is wrong.")
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