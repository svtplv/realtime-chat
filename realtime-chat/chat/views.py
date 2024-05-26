from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import ChatGroup
from .forms import ChatMessageCreateForm


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public_chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()
    # if request.htmx:
    #     form = ChatMessageCreateForm(request.POST)
    #     if form.is_valid:
    #         message = form.save(commit=False)
    #         message.author = request.user
    #         message.group = chat_group
    #         message.save()
    #         context = {"message": message, "user": request.user}
    #         return render(
    #             request, "chat/partials/chat_message_p.html", context
    #         )

    return render(
        request,
        "chat/chat.html",
        {"chat_messages": chat_messages, "form": form},
    )
