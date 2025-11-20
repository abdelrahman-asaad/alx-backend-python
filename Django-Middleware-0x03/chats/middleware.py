import logging
from datetime import datetime

# إعداد Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#logger is an instance of logging.Logger

# إعداد File Handler
file_handler = logging.FileHandler('requests.log') #to log requests to requests.log file
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # حفظ المرجع للـ view أو middleware التالي
        self.get_response = get_response

    def __call__(self, request):
        # ------------------------------
        # 1. قبل معالجة الـ view
        # ------------------------------
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # تنفيذ الـ view
        response = self.get_response(request)

        # ------------------------------
        # 2. بعد معالجة الـ view (اختياري)
        # ------------------------------
        return response

#__________________________________
from datetime import datetime, time
from django.http import JsonResponse


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to chat outside allowed hours.
    Allowed hours: 6 PM → 9 PM (18:00 → 21:00)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Define allowed time range
        start_time = time(18, 0)  # 6 PM
        end_time = time(21, 0)    # 9 PM

        now = datetime.now().time()

        # Check if within allowed time
        if not (start_time <= now <= end_time):
            # Deny access ONLY for chat URLs
            if request.path.startswith("/api/chats/"):
                return JsonResponse(
                    {
                        "error": "Access to chat is restricted between 9 PM and 6 PM.",
                        "allowed_time": "6 PM to 9 PM only"
                    },
                    status=403
                )

        # Continue normal flow
        return self.get_response(request)
