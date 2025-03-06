from django.urls import path
from .consumers import CommentConsumer

urlpatterns = [
    path('ws/comment-consumer/<book_slug>/', CommentConsumer.as_asgi())
]