# messaging/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# 2️⃣ Custom Manager
#class UnreadMessagesManager(models.Manager):
#    def for_user(self, user):
#        return self.filter(receiver=user, read=False).only('id', 'content', 'sender', 'timestamp')

from .managers import UnreadMessagesManager


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages") #to access received messages from same user model
    content = models.TextField()
    edited = models.BooleanField(default=False)  # New field
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    read = models.BooleanField(default=False)  # هل الرسالة مقروءة


    # New field for threaded conversations (replying to another message)
    parent_message = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='replies'      # to access replies of a parent message
    )



 # Managers
    objects = models.Manager()          # default manager
    unread = UnreadMessagesManager()    # custom manager ..>> we can do Message.unread.for_user(user) in views


    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"

    def get_threaded_replies(self):
        """
        Recursive function to fetch all replies in a threaded manner
        """
        all_replies = []

        def fetch_replies(message):
            for reply in message.replies.all():
                all_replies.append(reply)
                fetch_replies(reply) # هنا بنجيب الردود على الرد  nested replies

        fetch_replies(self)
        return all_replies

#message.id = 5
#message.replies.all() → كل الرسائل اللي parent_message_id = 5


# Optional: Use prefetch_related in views to optimize queries
# Example in a view:
# messages = Message.objects.filter(parent_message__isnull=True)\
#     .select_related('sender', 'receiver')\
#     .prefetch_related('replies__sender', 'replies__receiver')


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"

class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)