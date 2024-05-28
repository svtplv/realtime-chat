from django.forms import ModelForm
from django import forms

from .models import ChatGroup, GroupMessage


class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Message ...",
                    "class": "p-4 text-black",
                    "maxlength": "300",
                    "autofocus": True,
                }
            )
        }


class NewGroupChatForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["custom_name"]
        widgets = {
            "custom_name": forms.TextInput(
                attrs={
                    "placeholder": "Add name ...",
                    "class": "p-4 text-black",
                    "maxlength": "300",
                    "autofocus": True,
                }
            )
        }
