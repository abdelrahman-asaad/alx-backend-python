from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

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