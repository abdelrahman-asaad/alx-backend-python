from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Conversation, Message
from rest_framework_simplejwt.tokens import RefreshToken

# ------------------- UserSerializer -------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'role', 'created_at'
        ]

# ------------------- RegisterSerializer -------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'first_name', 'last_name',
            'phone_number', 'role'
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# ------------------- LoginSerializer -------------------
#there is no need for a custom LoginSerializer as we are using JWT default views
# so it returns tokens directly without needing a serializer here to get user credentials like username 
# and password with the tokens.
# ------------------- MessageSerializer -------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body_field = serializers.CharField(source='message_body', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'message_body_field']

# ------------------- ConversationSerializer -------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'message_count']

    def get_message_count(self, obj):
        return obj.messages.count()

    def validate(self, data):
        if self.instance and self.instance.participants.count() == 0:
            raise serializers.ValidationError("Conversation must have at least one participant.")
        return data


#_______________________________________ Example JSON Output _______________________________________

'''{
  "conversation_id": "c7c01a9b-22d4-4f09-8357-2a7a8c5d12f7",
  "participants": [
    {
      "user_id": "d4b2a78e-29e4-42b0-9bb0-5e8e0b2362af",
      "first_name": "Ali",
      "last_name": "Hassan",
      "email": "ali@example.com",
      "phone_number": "+201000000000",
      "role": "guest",
      "created_at": "2025-10-28T14:23:15Z"
    },
    {
      "user_id": "9f781b6e-1c3c-40a2-9371-3ad61de99af0",
      "first_name": "Sara",
      "last_name": "Ibrahim",
      "email": "sara@example.com",
      "phone_number": "+201111111111",
      "role": "host",
      "created_at": "2025-10-27T09:42:01Z"
    }
  ],
  "messages": [
    {
      "message_id": "1e3a8f87-66b3-48c1-bcf9-05ce89b93d76",
      "sender": {
        "user_id": "d4b2a78e-29e4-42b0-9bb0-5e8e0b2362af",
        "first_name": "Ali",
        "last_name": "Hassan",
        "email": "ali@example.com",
        "phone_number": "+201000000000",
        "role": "guest",
        "created_at": "2025-10-28T14:23:15Z"
      },
      "message_body": "Hi Sara! How are you?",
      "sent_at": "2025-10-29T13:00:00Z"
    },
    {
      "message_id": "2b7f64e1-48d4-4a40-85d0-7a0b9b7d9a93",
      "sender": {
        "user_id": "9f781b6e-1c3c-40a2-9371-3ad61de99af0",
        "first_name": "Sara",
        "last_name": "Ibrahim",
        "email": "sara@example.com",
        "phone_number": "+201111111111",
        "role": "host",
        "created_at": "2025-10-27T09:42:01Z"
      },
      "message_body": "Hey Ali! I'm good, thanks!",
      "sent_at": "2025-10-29T13:05:00Z"
    }
  ],
  "created_at": "2025-10-29T12:45:00Z"
}
'''