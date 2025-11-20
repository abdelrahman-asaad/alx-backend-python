from rest_framework import permissions
from rest_framework.permissions import BasePermission

#BasePermission is the base class for all custom permission classes in Django REST Framework.

class IsOwnerOfConversation(BasePermission):
    """
    Ensure the requesting user is a participant in the conversation
    """

    def has_object_permission(self, request, view, obj):
        # obj → Conversation instance
        return request.user in obj.participants.all()


class IsMessageOwner(BasePermission):
    """
    Ensure users can only see their own messages or messages in conversations they belong to
    """

    def has_object_permission(self, request, view, obj):
        # obj → Message instance
        return (
            request.user == obj.sender  # هو اللي بعت الرسالة
            or request.user in obj.conversation.participants.all()  # أو جزء من المحادثة
        )

#has_object_permission is built-in method in Django REST Framework's permission classes.
#it is called to check permissions against a specific object instance.
#for example, when retrieving, updating, or deleting a specific message or conversation,
#ensuring that the user has the right to perform actions on that particular instance.
# This is different from has_permission, which checks general permissions such as whether the user is
# authenticated to access a view at all, regardless of any specific object.

class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated users who are participants
    in the conversation to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj will be:
        - Conversation instance
        - Message instance
        """

        user = request.user

        # Check HTTP methods explicitly (requested by checker)
        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        if request.method not in allowed_methods:
            return False

        # If obj = Message → get conversation
        if hasattr(obj, "conversation"):
            conversation = obj.conversation  #message.conversation
        else:
            conversation = obj

        # Check if user is participant
        return user in conversation.participants.all()
    
    #message.conversation is used to access the Conversation instance associated with a Message instance.
    # and thats because in the Message model, there is a ForeignKey field named conversation that
    #  links each message to its corresponding conversation.
    # class Message(models.Model):
    #     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    # By using message.conversation, we can retrieve the Conversation object that the message belongs to
# and then check if the requesting user is a participant in that conversation.

#hasattr(obj, "conversation") is used to check if the obj (which can be either a Message or Conversation
# instance) has an attribute named conversation. like in message model we have a ForeignKey field named 
# conversation.