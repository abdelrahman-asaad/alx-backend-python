from rest_framework import permissions, BasePermission

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