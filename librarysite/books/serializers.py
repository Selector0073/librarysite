from rest_framework import serializers
from .models import books
from rest_framework.renderers import JSONRenderer



class booksModel:
    def __init__(self, title, img, reviews, content, upc, producttype, price, pricetax, tax, availability, reviewscount, ganres):
        self.title = title
        self.img = img
        self.reviews = reviews
        self.content = content
        self.upc = upc
        self.producttype = producttype
        self.price = price
        self.pricetax = pricetax
        self.tax = tax
        self.availability = availability
        self.reviewscount = reviewscount
        self.ganres = ganres




class booksSerializer(serializers.Serializer):
    title = serializers.CharField()
    img = serializers.CharField()
    reviews = serializers.IntegerField()
    content = serializers.CharField()
    upc = serializers.CharField()
    producttype = serializers.CharField()
    price = serializers.DecimalField(decimal_places=2, max_digits=10)
    pricetax = serializers.DecimalField(decimal_places=2, max_digits=10)
    tax = serializers.DecimalField(decimal_places=2, max_digits=10)
    availability = serializers.IntegerField()
    reviewscount = serializers.IntegerField()
    ganres = serializers.IntegerField(min_value=1, max_value=51)


def encode():
    data = {
        "title": "test",
        "img": "test",
        "reviews": 1,
        "content": "test",
        "upc": "123",
        "producttype": "book",
        "price": 10.50,
        "pricetax": 12.00,
        "tax": 1.50,
        "availability": 5,
        "reviewscount": 100,
        "ganres": 52
    }
    model_sr = booksSerializer(data=data)
    model_sr.is_valid()
    print(model_sr.validated_data)
    json = JSONRenderer().render(model_sr.data)
    print(json)

def decode():
    stream = io.BytexIO(b'{"title": "test", "img": "test", "reviews": 1, "content": "test", "upc": "123", "producttype": "book", "price": 10.50, "pricetax": 12.00, "tax": 1.50, "availability": 5, "reviewscount": 100, "ganres": 52}')
    data = JSONParser().parse(stream)
    serializer = booksSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)