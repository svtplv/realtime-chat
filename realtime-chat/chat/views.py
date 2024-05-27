from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ChatGroup
from .forms import ChatMessageCreateForm


User = get_user_model()


@login_required
def chat_view(request, chatroom_name="public_chat", other_user=None):
    chat_group = get_object_or_404(
        ChatGroup.objects.prefetch_related("chat_messages", "members"),
        group_name=chatroom_name,
    )
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        other_user = chat_group.members.all().exclude(
            id=request.user.id
        ).first()

    context = {
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
    }

    return render(request, "chat/chat.html", context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect("home")
    other_user = User.objects.get(username=username)
    chatroom = (
        ChatGroup.objects.filter(members=request.user, is_private=True)
        .filter(members=other_user)
        .first()
    )
    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect("chatroom", chatroom.group_name)
