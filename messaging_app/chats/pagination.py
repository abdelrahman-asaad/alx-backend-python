from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # عدد العناصر لكل صفحة
    page_size_query_param = "page_size"  # يسمح بتغيير عدد الرسائل عن طريق query param
    max_page_size = 100  # الحد الأقصى المسموح به
