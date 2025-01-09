from django.urls import path
from .views import home, upload_books, dashboard_books

urlpatterns = [
    path("books/", home, name="home"),
    path("dashboard/", dashboard_books, name="dashboard_books"),
    path("upload/", upload_books, name="upload_books"),
]
