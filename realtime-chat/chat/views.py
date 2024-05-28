from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ChatGroup, GroupMessage
from .forms import ChatMessageCreateForm, NewGroupChatForm


User = get_user_model()


@login_required
def chat_view(request, chatroom_name="public_chat", other_user=None):

    if chatroom_name == "public_chat":
        chat_messages = GroupMessage.objects.filter(
            group__group_name=chatroom_name
        ).select_related("author__profile")

    else:
        chat_group = get_object_or_404(
            ChatGroup.objects.prefetch_related("members"),
            group_name=chatroom_name,
        )
        chat_messages = GroupMessage.objects.filter(
            group=chat_group.id
        ).select_related("author__profile")

        if chat_group.is_private:
            if request.user not in chat_group.members.all():
                raise Http404()
            (other_user,) = (
                member
                for member in chat_group.members.all()
                if member != request.user
            )

    form = ChatMessageCreateForm()
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


@login_required
def create_groupchat(request):
    form = NewGroupChatForm()

    if request.method == "POST":
        form = NewGroupChatForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect("chatroom", new_groupchat.group_name)

    context = {"form": form}
    return render(request, "chat/create_groupchat.html", context)


@login_required
def get_user_chats(request):
    if request.htmx:
        chatrooms = request.user.chat_groups.all()
        context = {"chatrooms": chatrooms}
        return render(request, "chat/partials/user_chats_p.html", context)