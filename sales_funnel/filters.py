from rest_framework.pagination import PageNumberPagination
from .models import NewsletterSubscription
import django_filters

class DefaultPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'

class NewsletterSubscriptionFilter(django_filters.FilterSet):
    subscriptor_email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = NewsletterSubscription
        fields = ['subscriptor_email']