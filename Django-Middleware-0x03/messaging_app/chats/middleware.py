import logging
from datetime import datetime

# إعداد Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#logger is an instance of logging.Logger

# إعداد File Handler
file_handler = logging.FileHandler('requests.log') # سجل الطلبات في ملف requests.log
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



'''كل Logger عنده مستويات رسائل (Levels):

المستوى	           معنى الاستخدام
DEBUG    	تفاصيل صغيرة للتصحيح
INFO	معلومات عادية عن سير العمل
WARNING	     تحذيرات عن مشاكل محتملة
 ERROR           	خطأ حصل في النظام
CRITICAL	خطأ كبير ممكن يوقف النظام

لما نكتب:

logger.info(log_message)


معناه:

خذ الرسالة log_message

ضعها في مستوى INFO

أرسلها لكل handlers اللي مرتبطين بالـ Logger (في حالتنا FileHandler)

باختصار: هذا السطر هو اللي فعليًا “يطبع” الرسالة في أي مكان Logger متصل به.'''