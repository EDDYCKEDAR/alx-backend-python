# === messaging/views.py ===
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)
@login_required
def message_list_view(request):
    messages_list = Message.objects.filter(receiver=request.user).select_related('sender').prefetch_related('replies')
    return render(request, 'messaging/message_list.html', { 'messages': messages_list })

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('login')  # adjust redirect URL as needed
    return render(request, 'messaging/confirm_delete.html')
