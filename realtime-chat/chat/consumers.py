import json

from channels.generic.websocket import (
    AsyncWebsocketConsumer,
)
from django.shortcuts import aget_object_or_404
from django.template.loader import render_to_string

from .models import ChatGroup, GroupMessage


class ChatroomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        self.chatroom = await aget_object_or_404(
            ChatGroup.objects.prefetch_related("users_online"),
            group_name=self.chatroom_name,
        )
        await self.channel_layer.group_add(
            self.chatroom_name, self.channel_name
        )
        if self.user not in self.chatroom.users_online.all():
            await self.chatroom.users_online.aadd(self.user)
            await self.update_online_count()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chatroom_name, self.channel_name
        )
        if self.user in self.chatroom.users_online.all():
            await self.chatroom.users_online.aremove(self.user)
            await self.update_online_count()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]

        message = await GroupMessage.objects.acreate(
            body=body, author=self.user, group=self.chatroom
        )
        event = {"type": "message_handler", "message_id": message.id}
        await self.channel_layer.group_send(self.chatroom_name, event)

    async def message_handler(self, event):
        message_id = event["message_id"]
        message = await GroupMessage.objects.select_related(
            "author", "author__profile"
        ).aget(id=message_id)
        context = {"message": message, "user": self.user}
        html = render_to_string(
            "chat/partials/chat_message_p.html", context=context
        )
        await self.send(text_data=html)

    async def update_online_count(self):
        self.chatroom = await aget_object_or_404(
            ChatGroup.objects.prefetch_related("users_online"),
            pk=self.chatroom.pk,
        )
        online_count = await self.chatroom.users_online.acount() - 1
        event = {"type": "online_count_handler", "online_count": online_count}
        await self.channel_layer.group_send(self.chatroom_name, event)

    async def online_count_handler(self, event):
        online_count = event["online_count"]
        html = render_to_string(
            "chat/partials/online_count.html", {"online_count": online_count}
        )
        await self.send(text_data=html)
