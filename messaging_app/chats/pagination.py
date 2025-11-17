from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

#PageNumberPagination is a built-in pagination class in Django REST Framework that divides large result
# sets into manageable pages.

class MessagePagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,  
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
# Custom pagination class to paginate messages in conversations.
# It extends PageNumberPagination to set a default page size of 20 messages per page.

#get_paginated_response is overridden to customize the structure of the paginated response,
# including total count, next and previous links, and the actual results.