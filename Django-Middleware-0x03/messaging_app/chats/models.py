import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ✅ 1. Custom User Model (وراثة من AbstractUser)
class User(AbstractUser):
    """
    Custom User Model that extends Django's AbstractUser
    - نضيف الحقول اللي مش موجودة في الـ User الافتراضي
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(default=timezone.now)

    # Django بيستخدم username كـ REQUIRED_FIELD افتراضياً
    # فممكن نغيّر سلوك المصادقة ليستخدم الإيميل بدلاً من ذلك
    USERNAME_FIELD = 'email' # use email for authentication
    REQUIRED_FIELDS = ['username']  # username still required by Django to create superusers

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# ✅ 2. Conversation Model
class Conversation(models.Model):
    """
    Represents a chat conversation between two or more users
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# ✅ 3. Message Model
class Message(models.Model):
    """
    Represents a message sent by a user within a conversation
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
