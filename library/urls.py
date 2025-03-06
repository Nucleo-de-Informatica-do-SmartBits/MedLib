from django.urls import path
from .views import (
    home,
    dashboard,
    deleteBook,
    bookDetails,
    manageBook,
    readBook,
    add_suggestion,
    add_comment,
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("book/add/", manageBook, name="books-add"),
    path("book/<slug:slug>/edit/", manageBook, name="books-edit"),
    path("book/<slug:slug>/delete/", deleteBook, name="books-delete"),
    path("book/<slug>/<isbn>/", bookDetails, name="books-details"),
    path("read/<slug>/<isbn>/", readBook, name="read-book"),
    path("add-comment/", add_comment, name="add-comment"),
    path("add-suggestion/", add_suggestion, name="add-sugestion"),
]
