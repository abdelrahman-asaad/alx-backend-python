from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, MessageSerializer,
    UserSerializer, RegisterSerializer
)
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

# ------------------- Register -------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    return Response({
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)


# ------------------- Login -------------------
#there is no need for a custom login_view as we are using JWT default views provided by simplejwt
# which handle login and token generation automatically.

# ------------------- Logout -------------------
@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


# ------------------- Conversation ViewSet -------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------- Message ViewSet -------------------
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        return Message.objects.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = kwargs.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)




#perfrom_create is a built-in method in Django REST Framework's ModelViewSet that allows you to customize
# the creation behavior of an object when a POST request is made to create a new instance of serializer.
#we use 'perform_create' to set the sender to the logged-in user automatically when a message is created.
#it takes the serializer as an argument and calls its save method with the sender set to self.request.user.
