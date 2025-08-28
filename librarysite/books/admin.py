from django.contrib import admin
from .models import books, category
from user.models import users

admin.site.register(books)
admin.site.register(category)
admin.site.register(users)