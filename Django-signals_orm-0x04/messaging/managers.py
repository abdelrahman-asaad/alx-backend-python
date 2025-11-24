# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # جلب الرسائل الغير مقروءة للمستخدم
        return self.filter(receiver=user, read=False).only('id', 'content', 'sender', 'timestamp')
