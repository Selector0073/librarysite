from django.db import models

class books(models.Model):
    title = models.CharField()
    img = models.CharField()
    reviews = models.IntegerField()
    content = models.CharField()
    upc = models.CharField()
    producttype = models.CharField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    pricetax = models.DecimalField(decimal_places=2, max_digits=10)
    tax = models.DecimalField(decimal_places=2, max_digits=10)
    availability = models.IntegerField()
    reviewscount = models.IntegerField()
    ganres = models.ForeignKey('category', on_delete=models.PROTECT)
    date = models.DateField()

    def __str__(self):
        return self.title
    


class category(models.Model):
    genre = models.CharField(db_index=True)

    def __str__(self):
        return self.genre
    


class apikey(models.Model):
    apikey = models.CharField()

    def __str__(self):
        return self.apikey