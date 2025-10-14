import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_rating = django_filters.NumberFilter(field_name="average_rating", lookup_expr='gte')
    in_stock = django_filters.BooleanFilter(field_name="stock_quantity", lookup_expr='gt')
    
    class Meta:
        model = Book
        fields = ['category', 'genres', 'language', 'condition']