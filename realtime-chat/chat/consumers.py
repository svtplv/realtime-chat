from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from .models import ChatGroup


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        # self.user = self.scope["user"]
        # self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        # self.chatroom_name = get_object_or_404(
        #     ChatGroup, group_name=self.chatroom_name
        # )
        self.accept()
