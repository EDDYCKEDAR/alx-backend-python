from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated
        """
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is a participant in the conversation
        """
        # For Message objects, check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
            return conversation.participants.filter(id=request.user.id).exists()
        
        # For Conversation objects, check if user is a participant
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        
        return False


class IsMessageOwnerOrParticipant(BasePermission):
    """
    Custom permission that allows message owners to edit/delete their messages,
    and all participants to view messages.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated
        """
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        """
        Check permissions based on the action
        """
        # For viewing messages, check if user is participant in conversation
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.conversation.participants.filter(id=request.user.id).exists()
        
        # For editing/deleting messages, check if user is the message sender
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender == request.user
        
        # For creating messages, check if user is participant in conversation
        if request.method == 'POST':
            # This will be handled in the view since we don't have the object yet
            return True
        
        return False


class IsConversationParticipant(BasePermission):
    """
    Permission class specifically for conversation-level access
    """
    
    def has_permission(self, request, view):
        """
        Check if user is authenticated
        """
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user is a participant in the conversation
        """
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        
        return False


class CanCreateConversation(BasePermission):
    """
    Permission class for creating conversations
    """
    
    def has_permission(self, request, view):
        """
        Only authenticated users can create conversations
        """
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        
        return bool(request.user and request.user.is_authenticated)
