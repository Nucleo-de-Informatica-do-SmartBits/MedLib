from django.urls import path
from .views import home, dashboard, deleteBook, bookDetails, updateBook, addBook, sugest, get_book_data

urlpatterns = [
    path("books/", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("sugestion/", sugest, name="sugestion"),
    path("sugestion/", sugest, name="sugestion"),
    path("book/add", addBook, name="book-add"),
    path("book/delete/<slug:slug>/", deleteBook, name="book-delete"),
    path("book/update/<slug:slug>/", updateBook, name="book-update"),
    path("book/<slug:slug>/", bookDetails, name="book-details"),
    path("book/get-data/<slug:slug>", get_book_data, name="get_book_data"),
]

