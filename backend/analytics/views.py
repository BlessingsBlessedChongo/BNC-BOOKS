from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Avg, Q
from django.db import transaction
from django.utils import timezone
from datetime import timedelta, datetime 
import json

from books.models import Book
from orders.models import Order, OrderItem
from .models import SellerAnalytics, DailySales, BookPerformance, InventoryAlert, SalesReport
from .serializers import (
    SellerAnalyticsSerializer, BookPerformanceSerializer,
    InventoryAlertSerializer, SalesReportSerializer,
    CreateSalesReportSerializer, SellerDashboardSerializer
)

class SellerAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Ensure user is a seller
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can access analytics'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get or create seller analytics
        analytics, created = SellerAnalytics.objects.get_or_create(seller=request.user)
        
        # Update analytics data
        self._update_seller_analytics(request.user)
        
        # Refresh the analytics object
        analytics.refresh_from_db()
        
        serializer = SellerAnalyticsSerializer(analytics)
        return Response(serializer.data)
    
    def _update_seller_analytics(self, seller):
        """Update seller analytics with current data"""
        with transaction.atomic():
            analytics, created = SellerAnalytics.objects.get_or_create(seller=seller)
            
            # Calculate total revenue from orders
            total_revenue = OrderItem.objects.filter(
                book__seller=seller,
                order__status__in=['delivered', 'shipped', 'processing']
            ).aggregate(total=Sum('total_price'))['total'] or 0
            
            # Calculate total orders
            total_orders = Order.objects.filter(
                items__book__seller=seller
            ).distinct().count()
            
            # Calculate total books sold
            total_books_sold = OrderItem.objects.filter(
                book__seller=seller,
                order__status__in=['delivered', 'shipped', 'processing']
            ).aggregate(total=Sum('quantity'))['total'] or 0
            
            # Calculate total books listed
            total_books = Book.objects.filter(seller=seller).count()
            
            # Calculate conversion rate (simplified)
            total_views = BookPerformance.objects.filter(
                book__seller=seller
            ).aggregate(total=Sum('views'))['total'] or 0
            
            if total_views > 0:
                conversion_rate = (total_books_sold / total_views) * 100
            else:
                conversion_rate = 0
            
            # Update analytics
            analytics.total_revenue = total_revenue
            analytics.total_orders = total_orders
            analytics.total_books_sold = total_books_sold
            analytics.total_books = total_books
            analytics.total_views = total_views
            analytics.conversion_rate = round(conversion_rate, 2)
            
            if total_orders > 0:
                analytics.average_order_value = total_revenue / total_orders
            
            analytics.save()
            
            # Update daily sales for today
            self._update_daily_sales(seller)

class SellerOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can access seller orders'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get orders that include this seller's books
        orders = Order.objects.filter(
            items__book__seller=request.user
        ).distinct().order_by('-created_at')
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        # Paginate (simplified)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_orders = orders[start_idx:end_idx]
        
        from orders.serializers import OrderSerializer
        serializer = OrderSerializer(paginated_orders, many=True)
        
        return Response({
            'count': orders.count(),
            'results': serializer.data
        })
    
    def patch(self, request, order_id):
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can update orders'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get order that includes this seller's books
        order = get_object_or_404(
            Order, 
            pk=order_id, 
            items__book__seller=request.user
        )
        
        # Only allow updating status and tracking number
        allowed_fields = ['status', 'tracking_number']
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        if not update_data:
            return Response({
                'error': 'No valid fields to update'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update order status
        if 'status' in update_data:
            new_status = update_data['status']
            if new_status in ['shipped', 'delivered']:
                order.status = new_status
                if new_status == 'shipped' and not order.shipped_at:
                    order.shipped_at = timezone.now()
                elif new_status == 'delivered' and not order.delivered_at:
                    order.delivered_at = timezone.now()
        
        # Update tracking number if provided
        if 'tracking_number' in update_data:
            # In a real implementation, you might want to store this per seller
            pass
        
        order.save()
        
        from orders.serializers import OrderSerializer
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class BookPerformanceView(ListAPIView):
    serializer_class = BookPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role != 'seller':
            return BookPerformance.objects.none()
        
        return BookPerformance.objects.filter(
            book__seller=self.request.user
        ).select_related('book')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add summary statistics
        queryset = self.get_queryset()
        total_views = queryset.aggregate(total=Sum('views'))['total'] or 0
        total_revenue = queryset.aggregate(total=Sum('revenue'))['total'] or 0
        total_purchases = queryset.aggregate(total=Sum('purchases'))['total'] or 0
        
        response.data = {
            'summary': {
                'total_views': total_views,
                'total_revenue': float(total_revenue),
                'total_purchases': total_purchases,
                'average_conversion_rate': queryset.aggregate(avg=Avg('conversion_rate'))['avg'] or 0
            },
            'books': response.data
        }
        
        return response

class InventoryAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can access inventory alerts'
            }, status=status.HTTP_403_FORBIDDEN)
        
        alerts = InventoryAlert.objects.filter(
            seller=request.user
        ).order_by('-created_at')
        
        # Filter by resolved status if provided
        resolved_filter = request.query_params.get('resolved')
        if resolved_filter is not None:
            is_resolved = resolved_filter.lower() == 'true'
            alerts = alerts.filter(is_resolved=is_resolved)
        
        serializer = InventoryAlertSerializer(alerts, many=True)
        return Response(serializer.data)
    
    def post(self, request, alert_id):
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can manage inventory alerts'
            }, status=status.HTTP_403_FORBIDDEN)
        
        alert = get_object_or_404(
            InventoryAlert, 
            pk=alert_id, 
            seller=request.user
        )
        
        # Mark alert as resolved
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        
        serializer = InventoryAlertSerializer(alert)
        return Response(serializer.data)

class GenerateSalesReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can generate sales reports'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateSalesReportSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start_date = data['start_date']
        end_date = data['end_date']
        
        # Generate sales report
        report = self._generate_sales_report(request.user, start_date, end_date, data['report_type'])
        
        response_serializer = SalesReportSerializer(report)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def _generate_sales_report(self, seller, start_date, end_date, report_type):
        """Generate a comprehensive sales report"""
        # Get orders in date range
        orders = Order.objects.filter(
            items__book__seller=seller,
            created_at__date__range=[start_date, end_date],
            status__in=['delivered', 'shipped', 'processing']
        ).distinct()
        
        # Calculate totals
        total_revenue = OrderItem.objects.filter(
            book__seller=seller,
            order__in=orders
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        total_orders = orders.count()
        
        total_books_sold = OrderItem.objects.filter(
            book__seller=seller,
            order__in=orders
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Get top selling books
        top_books = Book.objects.filter(
            seller=seller,
            orderitem__order__in=orders
        ).annotate(
            sales=Count('orderitem'),
            revenue=Sum('orderitem__total_price')
        ).order_by('-sales')[:10]
        
        top_books_data = []
        for book in top_books:
            top_books_data.append({
                'id': book.id,
                'title': book.title,
                'sales': book.sales,
                'revenue': float(book.revenue or 0)
            })
        
        # Get revenue by date
        revenue_by_date = []
        current_date = start_date
        while current_date <= end_date:
            daily_revenue = OrderItem.objects.filter(
                book__seller=seller,
                order__created_at__date=current_date,
                order__status__in=['delivered', 'shipped', 'processing']
            ).aggregate(total=Sum('total_price'))['total'] or 0
            
            revenue_by_date.append({
                'date': current_date.isoformat(),
                'revenue': float(daily_revenue)
            })
            
            current_date += timedelta(days=1)
        
        # Create sales report
        report = SalesReport.objects.create(
            seller=seller,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            total_revenue=total_revenue,
            total_orders=total_orders,
            total_books_sold=total_books_sold,
            average_order_value=average_order_value,
            top_selling_books=top_books_data,
            revenue_by_date=revenue_by_date
        )
        
        return report

class SellerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'seller':
            return Response({
                'error': 'Only sellers can access the dashboard'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Update analytics first
        analytics_view = SellerAnalyticsView()
        analytics_view._update_seller_analytics(request.user)
        
        # Generate inventory alerts
        self._generate_inventory_alerts(request.user)
        
        # Get analytics
        analytics, created = SellerAnalytics.objects.get_or_create(seller=request.user)
        
        dashboard_data = {
            'overview': analytics,
            'recent_orders': [],
            'inventory_alerts': [],
            'top_performing_books': []
        }
        
        serializer = SellerDashboardSerializer(dashboard_data, context={'request': request})
        return Response(serializer.data)
    
    def _generate_inventory_alerts(self, seller):
        """Generate inventory alerts for seller's books"""
        books = Book.objects.filter(seller=seller, is_published=True)
        
        for book in books:
            # Check for low stock
            if book.stock_quantity <= 10 and book.stock_quantity > 0:
                alert, created = InventoryAlert.objects.get_or_create(
                    seller=seller,
                    book=book,
                    alert_type='low_stock',
                    is_resolved=False,
                    defaults={
                        'priority': 'high' if book.stock_quantity <= 3 else 'medium',
                        'message': f'Low stock alert: Only {book.stock_quantity} units left of "{book.title}"',
                        'current_stock': book.stock_quantity,
                        'threshold': 10
                    }
                )
            
            # Check for out of stock
            elif book.stock_quantity == 0:
                alert, created = InventoryAlert.objects.get_or_create(
                    seller=seller,
                    book=book,
                    alert_type='out_of_stock',
                    is_resolved=False,
                    defaults={
                        'priority': 'high',
                        'message': f'Out of stock: "{book.title}" has 0 units in inventory',
                        'current_stock': 0,
                        'threshold': 1
                    }
                )

    def _update_daily_sales(self, seller, analytics):
        """Update daily sales record for today"""
        today = timezone.now().date()
        
        # Calculate today's sales
        today_orders = Order.objects.filter(
            items__book__seller=seller,
            created_at__date=today,
            status__in=['delivered', 'shipped', 'processing']
        ).distinct()
        
        today_revenue = OrderItem.objects.filter(
            book__seller=seller,
            order__in=today_orders
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        today_orders_count = today_orders.count()
        
        today_books_sold = OrderItem.objects.filter(
            book__seller=seller,
            order__in=today_orders
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        # Get or create daily sales record
        daily_sales, created = DailySales.objects.get_or_create(
            seller=seller,
            date=today,
            defaults={
                'revenue': today_revenue,
                'orders': today_orders_count,
                'books_sold': today_books_sold,
                'views': 0  # This would come from actual view tracking
            }
        )
        
        if not created:
            daily_sales.revenue = today_revenue
            daily_sales.orders = today_orders_count
            daily_sales.books_sold = today_books_sold
            daily_sales.save()