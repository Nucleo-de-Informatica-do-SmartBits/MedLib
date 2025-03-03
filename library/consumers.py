import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Comment, Book

User = get_user_model()


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return
        
        book_slug = self.scope["url_route"]["kwargs"]["book_slug"]

        self.book = await self.get_book_by_slug(book_slug)
        self.group_name = "comments_"+book_slug

        await self.accept()

        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("content")

        if not content:
            return

        comment = await self.create_comment(content)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "comment_handler",
                "id": comment.id,
                "content": comment.content,
                "userId": comment.user.id,
                "username": comment.user.username,
                "created_at": comment.created_at.isoformat(),
            }
        )

    async def comment_handler(self, event):
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "content": event["content"],
            "userId": event["userId"],
            "username": event["username"],
            "created_at": event["created_at"],
        }))

    @database_sync_to_async
    def create_comment(self, content):
        comment = Comment.objects.create(
            user=self.user, book=self.book, content=content
        )

        return comment

    @database_sync_to_async
    def get_book_by_slug(self, slug):
        return get_object_or_404(Book, slug=slug)
