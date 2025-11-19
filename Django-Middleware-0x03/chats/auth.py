'''ملف مسؤول عن login / token generation لو عاوزين custom logic'''
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def login_user(username, password):
    user = authenticate(username=username, password=password)
    if not user:
        return None
    return get_tokens_for_user(user)
