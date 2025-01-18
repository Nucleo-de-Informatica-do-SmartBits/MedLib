from django.urls import path
<<<<<<< HEAD
from .views import (
    home,
    dashboard,
    deleteBook,
    bookDetails,
    manageBook,
    getBookData,
    readBook
)
=======
from .views import home, dashboard, deleteBook, bookDetails, updateBook, addBook, sugest, get_book_data
>>>>>>> 5c3cb4b10f6c49db59d3f9bcdbf18d2cafab6f1c

urlpatterns = [
    path("books/", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
<<<<<<< HEAD
    path("book/add/", manageBook, name="books-add"),
    path("book/<slug:slug>/edit/", manageBook, name="books-edit"),
    path("book/<slug:slug>/delete/", deleteBook, name="books-delete"),
    path("book/<slug:slug>/", bookDetails, name="books-details"),
    path("book/<slug:slug>/data/", getBookData, name="books-get-data"),
    path("book/<slug:slug>/read/", readBook, name="books-read"),
=======
    path("sugestion/", sugest, name="sugestion"),
    path("book/add", addBook, name="book-add"),
    path("book/delete/<slug:slug>/", deleteBook, name="book-delete"),
    path("book/update/<slug:slug>/", updateBook, name="book-update"),
    path("book/<slug:slug>/", bookDetails, name="book-details"),
    path("book/get-data/<slug:slug>", get_book_data, name="get_book_data"),
>>>>>>> 5c3cb4b10f6c49db59d3f9bcdbf18d2cafab6f1c
]
