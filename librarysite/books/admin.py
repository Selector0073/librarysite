from django.contrib import admin
from .models import books, apikey, category

admin.site.register(books)
admin.site.register(apikey)
admin.site.register(category)