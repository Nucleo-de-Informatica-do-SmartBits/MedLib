from django.urls import path
from .views import home, dashboard, deleteBook, bookDetails, updateBook, addBook

urlpatterns = [
    path("books/", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("book/add", addBook, name="book-add"),
    path("book/delete/<slug:slug>/", deleteBook, name="book-delete"),
    path("book/update/<slug:slug>/", updateBook, name="book-update"),
    path("book/<slug:slug>/", bookDetails, name="book-details"),
]

