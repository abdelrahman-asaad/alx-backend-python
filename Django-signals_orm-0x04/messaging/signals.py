from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth import get_user_model

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    قبل ما نعمل save للرسالة، نشوف هل اتعدلت ولا لا:
    - لو الرسالة موجودة قبل كده (instance.id موجود)
    - ولو محتواها الجدي مختلف عن القديم
    → نسجّل النسخة القديمة في MessageHistory
    """

    if not instance.id:  #= true because it hasn't been saved yet         #instance of Message model class 
        return           # skip the rest if it's a new message

    try:
        old_message = Message.objects.get(id=instance.id) # get the existing message from DB before save
    except Message.DoesNotExist:
        return

    # لو المحتوى اتغير فعلاً
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )

        # علّم الرسالة أنها اتعدلت
        instance.edited = True

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create notification for receiver
        Notification.objects.create(
            user=instance.receiver,         #instance of Message model class
            message=instance,
            edited_by=instance.sender  # or request.user if available in context

        )

User = get_user_model()
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    When a user is deleted:
    - Delete all messages sent or received by the user
    - Delete all notifications related to the user
    - Delete all message history associated with the user's messages
    """
    # حذف الـ Messages المرتبطة بالمستخدم
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # حذف الـ Notifications المرتبطة بالمستخدم
    Notification.objects.filter(user=instance).delete()

    # حذف الـ MessageHistory المرتبط بأي رسالة كانت للمستخدم
    MessageHistory.objects.filter(message__sender=instance).delete()
