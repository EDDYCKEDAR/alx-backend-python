from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'created_at']

    def validate_message_body(self, value):
        if not value.strip():
            raise ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'last_message']

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        return last.message_body if last else None
