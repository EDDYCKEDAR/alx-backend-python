from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework.exceptions import ValidationError

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)  # ← includes CharField

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

# ✅ Message Serializer with validation
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    message_body = serializers.CharField()  # ← includes CharField

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'created_at']

    # 🔒 Custom validation using ValidationError
    def validate_message_body(self, value):
        if not value.strip():
            raise ValidationError("Message body cannot be empty.")
        return value

# ✅ Conversation Serializer with nested messages & computed field
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    # 🧠 SerializerMethodField to get last message body
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'last_message']

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        return last.message_body if last else None
