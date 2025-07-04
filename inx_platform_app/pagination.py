# pagination.py
from rest_framework.pagination import PageNumberPagination

class LargeResultSetPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 10000