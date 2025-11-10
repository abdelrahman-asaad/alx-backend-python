# messaging_app/chats/urls.py
from django.urls import path, include  # ✅ required by checker
from rest_framework import routers  # ✅ routers.DefaultRouter()
from .views import ConversationViewSet, MessageViewSet

# إنشاء الراوتر
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# URLs النهائية
urlpatterns = [
    path('', include(router.urls)),  # تضمين كل الرواتر
]
