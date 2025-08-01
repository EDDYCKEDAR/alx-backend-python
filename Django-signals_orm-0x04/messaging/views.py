# === messaging/views.py ===
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import Message
from .managers import UnreadMessagesManager  # Ensure this is imported

@cache_page(60)
@login_required
def message_list_view(request):
    messages_list = Message.unread.unread_for_user(request.user).only('id', 'content', 'sender', 'created_at').select_related('sender').prefetch_related('replies')
    sent_messages = Message.objects.filter(sender=request.user).only('id', 'content', 'receiver', 'created_at').select_related('receiver').prefetch_related('replies')
    return render(request, 'messaging/message_list.html', {
        'messages': messages_list,
        'sent_messages': sent_messages
    })

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('login')  # adjust redirect URL as needed
    return render(request, 'messaging/confirm_delete.html')
