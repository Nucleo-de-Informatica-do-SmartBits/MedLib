from django.contrib import admin
from .models import Author, Book, Category, Publisher, Sugestion

# Register your models here.
admin.site.register([Author, Book, Category, Publisher, Sugestion])
