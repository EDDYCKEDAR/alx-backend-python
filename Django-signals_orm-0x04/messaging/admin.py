# === messaging/admin.py ===
from django.contrib import admin
from .models import Message, Notification, MessageHistory

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)


# === messaging/views.py ===
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from .models import Message

@cache_page(60)
@login_required
def message_list_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender').prefetch_related('replies')
    return render(request, 'messaging/message_list.html', { 'messages': messages })
