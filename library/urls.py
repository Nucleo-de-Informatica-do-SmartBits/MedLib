from django.urls import path
from .views import (
    home,
    dashboard,
    deleteBook,
    bookDetails,
    manageBook,
    readBook,
    sugest,
    add_comment,
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("book/add/", manageBook, name="books-add"),
    path("book/<slug:slug>/edit/", manageBook, name="books-edit"),
    path("book/<slug:slug>/delete/", deleteBook, name="books-delete"),
    path("book/<slug:slug>/", bookDetails, name="books-details"),
    path("book/<slug:slug>/read/", readBook, name="books-read"),
    path("add-comment/", add_comment, name="add-comment"),
    path("sugestion/", sugest, name="sugestion"),
]
