# messaging/serializers.py
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id',
            'content',
            'edited',
            'timestamp',
            'sender',
            'sender_name',
            'receiver',
            'receiver_name',
            'parent_message',
            'conversation',
        ]
        read_only_fields = ['id', 'edited', 'timestamp', 'sender', 'sender_name', 'receiver_name']
