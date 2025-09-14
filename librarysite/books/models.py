from django.db import models
from django.core.validators import MinValueValidator
from common.models import ModelMixin



class Book(ModelMixin, models.Model):
    title = models.CharField(unique=True)
    img = models.URLField()
    reviews = models.IntegerField(validators=[MinValueValidator(0)])
    content = models.CharField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    availability = models.IntegerField(validators=[MinValueValidator(0)])
    reviews_count = models.IntegerField(validators=[MinValueValidator(0)])
    genre = models.ForeignKey('Category', on_delete=models.PROTECT)
    date = models.DateField()

    def __str__(self):
        return self.title



class Category(models.Model):
    genre = models.CharField(db_index=True)

    def __str__(self):
        return self.genre
    