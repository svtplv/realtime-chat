from django.contrib.auth import get_user_model
from django.db import models
import shortuuid


User = get_user_model()


class ChatGroup(models.Model):
    group_name = models.CharField(
        max_length=128, unique=True, default=shortuuid.uuid
    )
    custom_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(
        User,
        related_name="groupchats",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    members = models.ManyToManyField(
        User, related_name="chat_groups", blank=True
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(
        ChatGroup, related_name="chat_messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.author.username} : {self.body}"
