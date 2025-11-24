# chats/views.py

from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@cache_page(60)  # cache for 60 seconds
def conversation_messages_view(request, conversation_id):
    """
    Retrieve all messages in a conversation, cached for 60 seconds.
    """
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

#many=True because we are serializing a queryset of multiple messages