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



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'availability', 'price'
        ]



class BookDetailsSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Book
        fields = [
            'title', 'img', 'reviews', 'content', 'price', 'availability', 'reviews_count', 'genre', 'writed_at', 'author'
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mode = self.context.get("mode")

        if mode == "ExportBooksExcel":
            self.fields["title"].required = False
            self.fields["img"].required = False
            self.fields["reviews"].required = False
            self.fields["content"].required = False
            self.fields["price"].required = False
            self.fields["availability"].required = False
            self.fields["reviews_count"].required = False
            self.fields["genre"].required = False
            self.fields["writed_at"].required = False
            self.fields["author"].required = False

        elif mode == "RedactBook":
            self.fields["title"].required = True
            self.fields["img"].required = False
            self.fields["reviews"].required = False
            self.fields["content"].required = False
            self.fields["price"].required = False
            self.fields["availability"].required = False
            self.fields["reviews_count"].required = False
            self.fields["genre"].required = False
            self.fields["writed_at"].required = False
            self.fields["author"].required = False

    def GetData(self):
        genre = self.validated_data.get("genre")
        title = self.validated_data.get("title")
        if genre and title:
            raise serializers.ValidationError("Only one filter must be provided")
        elif genre:
            return Book.objects.filter(genre=genre)
        elif title:
            return Book.objects.filter(title=title)
        else:
            return Book.objects.all()


    def validate_title(self, value):
        mode = self.context.get("mode")
        if mode == "RedactBook":
            if not Book.objects.filter(title=value).exists():
                raise serializers.ValidationError("Book with this title not found.")
            else:
                book = Book.objects.get(title=value)
                self.instance = book
            return value



    def save(self, **kwargs):
        if not hasattr(self, 'instance') or not self.instance:
            raise RuntimeError("Book instance not found. 'validate_title' must be called first.")
        for attr, value in self.validated_data.items():
            setattr(self.instance, attr, value)
        self.instance.save()
        return self.instance
