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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def conversation_threaded_view(request, conversation):
    """
    GET: Retrieve all top-level messages in a conversation along with threaded replies.
    POST: Create a new message in this conversation.
    """
    if request.method == 'POST':
        parent_id = request.data.get('parent_message')
        content = request.data.get('content')
        receiver_id = request.data.get('receiver')

       # to get receiver user instance
        receiver_user = User.objects.get(id=receiver_id)
        parent_message = None
        if parent_id:
            parent_message = Message.objects.get(id=parent_id)

        # إنشاء الرسالة مع sender من request.user ← هذا المطلوب
        new_msg = Message.objects.create(
            content=content,
            sender=request.user,
            receiver=receiver_user,
            conversation=conversation,
            parent_message=parent_message
        )

        return Response(MessageSerializer(new_msg).data, status=201) 
    

    # لو GET
    top_messages = (
        Message.objects.filter(conversation=conversation, parent_message__isnull=True) #top-level messages only
        .select_related('sender', 'receiver') #to get sender and receiver user data in same query
        .prefetch_related('replies__sender', 'replies__receiver') # to get replies and their senders/receivers
    )                                                             #replies = related_name of parent_message
                        #sender in replies__sender is the sender field in Message model
    
    data = []
    for msg in top_messages:
        data.append({
            "message": MessageSerializer(msg).data, #to serialize the top-level message 
            "replies": fetch_replies(msg)           #to get all its replies in nested structure
        })

    return Response(data)

#where "message" is the top-level message and "replies" is a list of its threaded replies
# and they are key-value pairs in a dictionary inside a list 

# Example response structure:
'''[
    {
        "message": { "id": 1, "content": "Hello", "sender": ..., "receiver": ..., ... },
        "replies": [
            {
                "reply": { "id": 2, "content": "Hi!", ... },
                "replies": [
                    { "reply": { ... }, "replies": [...] }
                ]
            }
        ]
    },
    {
        "message": { "id": 5, "content": "Another message", ... },
        "replies": []
    }
]
'''
#_______________________________________________
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages_view(request):
    unread_msgs = Message.unread.unread_for_user(request.user).only('id', 'content', 'sender', 'timestamp')
    serializer = MessageSerializer(unread_msgs, many=True) #serialize the queryset of unread messages
    return Response(serializer.data)
#only 'id', 'content', 'sender', 'timestamp' fields are fetched from DB instead of all fields .. so 
# it optimizes the query performance
#many=True because we are serializing a queryset (multiple messages)
#Retrieve all unread messages for the authenticated user.

#_______________week6_task5______________________
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
def conversation_messages_view(request, conversation):
    """
    Retrieve all messages in a conversation, cached for 60 seconds.
    """
    messages = Message.objects.filter(conversation=conversation).select_related('sender', 'receiver')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
#many=True because we are serializing a queryset of multiple messages
