from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/chats/', include('messaging_app.chats.urls')),
]

'''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),  # ✅ لتسجيل الدخول في Browsable API
    #/api-auth/login/
    #/api-auth/logout/

]



هذا يضيف واجهات تسجيل الدخول والخروج للـ browsable API الخاص بـ DRF.

أي URL موجود داخل /api-auth/ يسمح لك بـ:

تسجيل الدخول: /api-auth/login/

تسجيل الخروج: /api-auth/logout/

مفيد إذا تستخدم Browsable API أثناء التطوير أو الاختبار.

بدون هذا، لن تتمكن من تسجيل الدخول عبر واجهة المتصفح لاختبار الـ API protected بـ IsAuthenticated.'''