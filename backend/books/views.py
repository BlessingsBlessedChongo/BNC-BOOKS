from rest_framework import status, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import Book, Category, Genre
from .serializers import (
    BookListSerializer, BookDetailSerializer, BookCreateSerializer,
    CategorySerializer, GenreSerializer, InventoryUpdateSerializer
)
from analytics.models import BookPerformance
from analytics.serializers import BookPerformanceSerializer
class SellerBookPerformanceView(ListAPIView):
    serializer_class = BookPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BookPerformance.objects.filter(
            book__seller=self.request.user
        ).select_related('book')
class BookListView(ListAPIView):
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'isbn', 'description']
    filterset_fields = ['category', 'genres', 'language', 'condition']
    ordering_fields = ['title', 'price', 'average_rating', 'created_at', 'total_sales']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_published=True)
        
        # Apply custom filters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_rating = self.request.query_params.get('min_rating')
        in_stock = self.request.query_params.get('in_stock')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))
        if min_rating:
            queryset = queryset.filter(average_rating__gte=float(min_rating))
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset.select_related('category', 'seller').prefetch_related('genres')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add pagination metadata as per documentation
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            return self.get_paginated_response(response.data)
        
        return response

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.filter(is_published=True)
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.AllowAny]

class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        categories = Category.objects.all().values_list('name', flat=True)
        return Response({
            'categories': list(categories)
        })

class FeaturedBooksView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        featured_books = Book.objects.filter(
            is_published=True, 
            is_featured=True,
            stock_quantity__gt=0
        )[:8]
        
        serializer = BookListSerializer(featured_books, many=True)
        
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })

# Seller Management Views
class SellerBookListView(ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user)

class SellerBookCreateView(CreateAPIView):
    serializer_class = BookCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class SellerBookDetailView(RetrieveAPIView, UpdateAPIView):
    serializer_class = BookCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Book.objects.filter(seller=self.request.user)

class InventoryUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        try:
            book = Book.objects.get(pk=pk, seller=request.user)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = InventoryUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        adjustment_type = data.get('adjustment_type', 'set')
        
        if adjustment_type == 'set':
            book.stock_quantity = data['stock_quantity']
        elif adjustment_type == 'add':
            book.stock_quantity += data['adjustment_amount']
        elif adjustment_type == 'subtract':
            book.stock_quantity = max(0, book.stock_quantity - data['adjustment_amount'])
        
        book.save()
        
        return Response({
            'id': book.id,
            'stock_quantity': book.stock_quantity,
            'adjustment_type': adjustment_type,
            'adjustment_amount': data.get('adjustment_amount'),
            'reason': data.get('reason'),
            'notes': data.get('notes'),
            'updated_at': book.updated_at.isoformat()
        })