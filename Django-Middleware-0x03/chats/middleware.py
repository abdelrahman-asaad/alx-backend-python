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

#________________________________
from datetime import datetime, timedelta
from django.http import JsonResponse


class OffensiveLanguageMiddleware:
    """
    Limits chat messages from the same IP address.
    Maximum: 5 messages per minute.
    """

    # Static in-memory store
    ip_requests = {}             #represents a dictionary to store request timestamps per IP , such as {'123.456.789.000': [datetime1, datetime2, ...]}

#ip_requests = {user_ip: [timestamp1, timestamp2, ...]} where user_ip is the 'KEY' and the 'VALUE' is a list of datetime objects representing the times of the requests from that IP address.

#and it is middleware instance variable to keep track of request timestamps for each IP address.
    
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Only apply to POST requests to chat APIs
        if request.method == "POST" and request.path.startswith("/api/chats/"):

            user_ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean old entries
            if user_ip not in self.ip_requests:
                self.ip_requests[user_ip] = []

            # Keep only requests in the last 1 minute (filtering)
            one_minute_ago = now - timedelta(minutes=1) #one_minute_ago equals the current time minus one minute such as if now is 12:05, one_minute_ago will be 12:04 , any timestamp older than that will be removed from the list
            self.ip_requests[user_ip] = [
                time for time in self.ip_requests[user_ip] if time > one_minute_ago  #such as if the list had timestamps [12:03:40, 12:04:02, 12:04:18] and now is 12:05, after this line it will keep only [12:04:02, 12:04:18]
            ]

            # Check limit
            if len(self.ip_requests[user_ip]) >= 5:
                return JsonResponse(
                    {
                        "error": "Message rate limit exceeded. Max 5 messages per minute.",
                        "limit": 5,
                        "time_window": "1 minute"
                    },
                    status=429
                )

            # Add the current request timestamp
            self.ip_requests[user_ip].append(now) #such as if now is 12:05:10, it will append that to the list of timestamps for that IP

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address (supports proxy)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


#get_client_ip is a helper method to extract the client's IP address from the request, 
# considering possible proxy headers.

#________________________________
from django.http import JsonResponse

class RolepermissionMiddleware:
    """
    Middleware to restrict access based on user role.
    Only 'admin' or 'moderator' users can proceed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip checking for unauthenticated users
        if request.user.is_authenticated:
            # get user role
            role = getattr(request.user, "role", None) #we use getattr to safely get the 'role' attribute of the user object and if it doesn't exist, it returns None instead of raising an error.

#reading the 'role' attribute from custom User model

            # Allow only admin or moderator
            if role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"detail": "You do not have permission to access this resource."},
                    status=403
                )

        # continue processing request
        response = self.get_response(request)
        return response
