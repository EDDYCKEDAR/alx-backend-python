from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter


from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import (
    IsConversationParticipant,
    IsMessageOwnerOrParticipant,
    CanCreateConversation,
)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant | CanCreateConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        # ✅ Only return conversations the user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if not participants:
            return Response({"error": "Participants list is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the current user is added as a participant if not already included
        if request.user.id not in participants:
            participants.append(request.user.id)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwnerOrParticipant]
     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['created_at']

    def get_queryset(self):
        # ✅ Only return messages from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({"error": "conversation_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, id=conversation_id)

        # ✅ Check if user is participant
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response({"detail": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['sender'] = request.user.pk
        data['conversation'] = conversation.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        if message.sender != request.user:
            return Response({"detail": "You can only delete your own messages."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
