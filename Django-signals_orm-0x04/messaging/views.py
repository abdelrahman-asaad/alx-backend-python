# messaging/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Delete the authenticated user's account.
    """
    user = request.user
    user.delete()
    return Response({"detail": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#_____________week6_task3______________________

# messaging/views.py
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Message, User
from .serializers import MessageSerializer

def fetch_replies(message):
    """Recursive function to get all replies of a message in a nested structure"""
    nested = []
    for reply in message.replies.all():  # replies = related_name of parent_message
        nested.append({
            "reply": MessageSerializer(reply).data,
            "replies": fetch_replies(reply)  # recursive for replies of replies
        })
    return nested

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_threaded_view(request, conversation_id):
    """
    Retrieve all top-level messages in a conversation along with threaded replies.
    """
    # جلب الرسائل الرئيسية فقط (parent_message=None)
    top_messages = (
        Message.objects.filter(conversation_id=conversation_id, parent_message__isnull=True)
        .select_related('sender', 'receiver')        # يقلل عدد الاستعلامات للFK
        .prefetch_related('replies__sender', 'replies__receiver')  # يقلل عدد الاستعلامات للردود
    )

    data = []
    for msg in top_messages:
        data.append({
            "message": MessageSerializer(msg).data,
            "replies": fetch_replies(msg)
        })

    return Response(data)
