from django.urls import path
from .views import home, dashboard, deleteBook, bookDetails

urlpatterns = [
    path("books/", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("book-details/<slug:slug>/", bookDetails, name="book-details"),
    path("delete-book/<slug:slug>/", deleteBook, name="delete-book"),
]

