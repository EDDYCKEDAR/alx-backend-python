from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageListView(APIView):
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
