from rest_framework import serializers
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from books.models import Book
from orders.models import Order, OrderItem
from .models import SellerAnalytics, DailySales, BookPerformance, InventoryAlert, SalesReport

class TopSellingBookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    sales = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class RevenueByPeriodSerializer(serializers.Serializer):
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class SellerAnalyticsSerializer(serializers.ModelSerializer):
    revenue_growth = serializers.SerializerMethodField()
    order_growth = serializers.SerializerMethodField()
    top_selling_books = serializers.SerializerMethodField()
    revenue_by_period = serializers.SerializerMethodField()
    average_commission = serializers.SerializerMethodField()
    
    class Meta:
        model = SellerAnalytics
        fields = (
            'total_revenue', 'revenue_growth', 'total_orders', 'order_growth',
            'total_books', 'conversion_rate', 'total_views', 'average_commission',
            'top_selling_books', 'revenue_by_period'
        )
    
    def get_revenue_growth(self, obj):
        return self._calculate_growth(obj, 'revenue')
    
    def get_order_growth(self, obj):
        return self._calculate_growth(obj, 'orders')
    
    def get_top_selling_books(self, obj):
        # Get top 5 selling books for this seller
        top_books = Book.objects.filter(
            seller=obj.seller,
            orderitem__isnull=False
        ).annotate(
            sales=Count('orderitem'),
            revenue=Sum('orderitem__total_price')
        ).order_by('-sales')[:5]
        
        return TopSellingBookSerializer(top_books, many=True).data
    
    def get_revenue_by_period(self, obj):
        # Get revenue for last 7 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=6)
        
        daily_sales = DailySales.objects.filter(
            seller=obj.seller,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        return RevenueByPeriodSerializer(daily_sales, many=True).data
    
    def get_average_commission(self, obj):
        # Calculate average commission (for marketplace fee simulation)
        # This would typically come from your commission settings
        return 12.50
    
    def _calculate_growth(self, obj, metric):
        # Calculate growth compared to previous period
        end_date = timezone.now().date()
        start_date_current = end_date - timedelta(days=30)
        start_date_previous = start_date_current - timedelta(days=30)
        
        if metric == 'revenue':
            current_period = DailySales.objects.filter(
                seller=obj.seller,
                date__range=[start_date_current, end_date]
            ).aggregate(total=Sum('revenue'))['total'] or 0
            
            previous_period = DailySales.objects.filter(
                seller=obj.seller,
                date__range=[start_date_previous, start_date_current - timedelta(days=1)]
            ).aggregate(total=Sum('revenue'))['total'] or 0
        else:  # orders
            current_period = DailySales.objects.filter(
                seller=obj.seller,
                date__range=[start_date_current, end_date]
            ).aggregate(total=Sum('orders'))['total'] or 0
            
            previous_period = DailySales.objects.filter(
                seller=obj.seller,
                date__range=[start_date_previous, start_date_current - timedelta(days=1)]
            ).aggregate(total=Sum('orders'))['total'] or 0
        
        if previous_period > 0:
            growth = ((current_period - previous_period) / previous_period) * 100
            return round(float(growth), 1)
        elif current_period > 0:
            return 100.0
        else:
            return 0.0

class BookPerformanceSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_price = serializers.DecimalField(source='book.price', read_only=True, max_digits=8, decimal_places=2)
    
    class Meta:
        model = BookPerformance
        fields = (
            'id', 'book', 'book_title', 'book_author', 'book_price',
            'views', 'add_to_cart_count', 'purchases', 'revenue',
            'conversion_rate', 'last_updated'
        )

class InventoryAlertSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    
    class Meta:
        model = InventoryAlert
        fields = (
            'id', 'book', 'book_title', 'book_author', 'alert_type',
            'priority', 'message', 'current_stock', 'threshold',
            'is_resolved', 'created_at', 'resolved_at'
        )

class SalesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReport
        fields = (
            'id', 'report_type', 'start_date', 'end_date',
            'total_revenue', 'total_orders', 'total_books_sold',
            'average_order_value', 'top_selling_books', 'revenue_by_date',
            'created_at'
        )

class CreateSalesReportSerializer(serializers.Serializer):
    report_type = serializers.ChoiceField(choices=SalesReport.REPORT_TYPES)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                'start_date': 'Start date must be before end date'
            })
        
        # Check if date range is reasonable
        date_range = (data['end_date'] - data['start_date']).days
        if date_range > 365:
            raise serializers.ValidationError({
                'end_date': 'Date range cannot exceed 1 year'
            })
        
        return data

class SellerDashboardSerializer(serializers.Serializer):
    overview = SellerAnalyticsSerializer()
    recent_orders = serializers.SerializerMethodField()
    inventory_alerts = serializers.SerializerMethodField()
    top_performing_books = serializers.SerializerMethodField()
    
    def get_recent_orders(self, obj):
        from orders.serializers import OrderSerializer
        recent_orders = Order.objects.filter(
            items__book__seller=obj
        ).distinct().order_by('-created_at')[:5]
        return OrderSerializer(recent_orders, many=True).data
    
    def get_inventory_alerts(self, obj):
        alerts = InventoryAlert.objects.filter(
            seller=obj,
            is_resolved=False
        ).order_by('-priority', '-created_at')[:10]
        return InventoryAlertSerializer(alerts, many=True).data
    
    def get_top_performing_books(self, obj):
        top_books = BookPerformance.objects.filter(
            book__seller=obj
        ).order_by('-revenue')[:5]
        return BookPerformanceSerializer(top_books, many=True).data