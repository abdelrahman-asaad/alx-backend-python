"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),  # ✅ لتسجيل الدخول في Browsable API
    #/api-auth/login/
    #/api-auth/logout/

]



'''هذا يضيف واجهات تسجيل الدخول والخروج للـ browsable API الخاص بـ DRF.

أي URL موجود داخل /api-auth/ يسمح لك بـ:

تسجيل الدخول: /api-auth/login/

تسجيل الخروج: /api-auth/logout/

مفيد إذا تستخدم Browsable API أثناء التطوير أو الاختبار.

بدون هذا، لن تتمكن من تسجيل الدخول عبر واجهة المتصفح لاختبار الـ API protected بـ IsAuthenticated.'''