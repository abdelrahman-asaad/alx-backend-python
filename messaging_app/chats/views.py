# messaging_app/chats/views.py
from rest_framework import viewsets, permissions, filters  # ✅ استيراد filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


# 1️⃣ Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    """
    إدارة المحادثات:
    - list: عرض كل المحادثات
    - create: إنشاء محادثة جديدة
    - retrieve: عرض محادثة واحدة مع رسائلها
    """
    queryset = Conversation.objects.all()  # كل المحادثات
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]  # تسجيل دخول مطلوب

    # تمكين البحث والفلترة حسب أسماء المشاركين
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']

    # Action مخصص لإرسال رسالة لمحادثة موجودة
    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        conversation = self.get_object()  # جلب المحادثة بواسطة pk
        serializer = MessageSerializer(data=request.data)  # بيانات الرسالة الجديدة
        if serializer.is_valid():  # التحقق من صحة البيانات
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=201)  # إعادة البيانات بعد الإنشاء
        return Response(serializer.errors, status=400)  # أخطاء التحقق


# 2️⃣ Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    """
    إدارة الرسائل:
    - list: عرض كل الرسائل
    - create: إرسال رسالة جديدة
    """
    queryset = Message.objects.all()  # كل الرسائل
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def perform_create(self, serializer):
        # ربط الرسالة بالمستخدم الحالي عند الإنشاء
        serializer.save(sender=self.request.user)


#perfrom_create is a built-in method in Django REST Framework's ModelViewSet that allows you to customize
# the creation behavior of an object when a POST request is made to create a new instance of serializer.
#we use 'perform_create' to set the sender to the logged-in user automatically when a message is created.
#it takes the serializer as an argument and calls its save method with the sender set to self.request.user.
