# messaging_app/chats/urls.py
from django.urls import path, include
from rest_framework_nested import routers  # ✅ NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from .views import register_view, logout_view

# رواتر رئيسية للمحادثات
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# رواتر nested للرسائل داخل كل محادثة
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# URLs النهائية
urlpatterns = [
    path('', include(router.urls)),  # روابط المحادثات الأساسية
    path('', include(conversations_router.urls)),  # روابط الرسائل المتداخلة
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
]
#there is no login view here because we are using the default JWT login view provided by simplejwt


'''✅ هنا أي رسالة مرتبطة بمحاضثة يمكن الوصول لها عبر:

/conversations/<conversation_id>/messages/

ex /api/conversations/1/messages/    ← كل الرسائل الخاصة بالمحادثة 1
ويمكن إنشاء رسالة جديدة في محادثة معينة عبر نفس الرابط باستخدام POST.

______________________________________

علي العكس لو ما استخدمناش nested router، هيكون عندنا رابط عام للرسائل زي:

/api/messages/         ← كل الرسائل في النظام
/api/conversations/    ← كل المحادثات

لكن مش هيكون في رابط مباشر يربط الرسائل بمحاضثاتها.
استخدام nested routers بيسهل تنظيم الـ API وبيعكس العلاقة بين المحادثات والرسائل بشكل أوضح.

وبالتالي كان ممكن نستخدم الرواتر العادية بس هيبقي أقل وضوح وتنظيم.

ذا أردت عرض رسائل محادثة معينة، تحتاج فلتر في query params:

/api/messages/?conversation=1

'''