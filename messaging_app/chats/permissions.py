from rest_framework import permissions, BasePermission, is_authenticated

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
    Allow access only to authenticated users
    AND only if they are part of the conversation.
    """

    def has_permission(self, request, view):
        # First: user must be authenticated
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        obj will be:
        - A Conversation instance in ConversationViewSet
        - A Message instance in MessageViewSet
        """

        user = request.user

        # If obj is a Message → Get its conversation
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
        else:
            conversation = obj

        # Check if user is a participant
        return user in conversation.participants.all()
