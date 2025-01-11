from django.contrib import admin
from .models import Author, Book, Category, Publisher

admin.site.register([Author, Book, Category, Publisher])
