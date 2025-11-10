from rest_framework import serializers
from .models import User, Conversation, Message


# ✅ 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    - هنستخدمه في كل العلاقات التانية (مثل المرسل والمشاركين)
    """
    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email',
            'phone_number', 'role', 'created_at'
        ]


# ✅ 2. Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages.
    - يضم بيانات المرسل nested (لكن بشكل مختصر)
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# ✅ 3. Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversations.
    - يحتوي على المشاركين (users)
    - ويعرض الرسائل (messages) الخاصة بالمحادثة نفسها
    """

    #nested serializers
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
