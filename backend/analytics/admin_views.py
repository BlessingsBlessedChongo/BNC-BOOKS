from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from books.models import Book, Category
from orders.models import Order, OrderItem
from affiliates.models import Affiliate, Commission
from reviews.models import Review
from analytics.models import SellerAnalytics

class PlatformAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if not request.user.is_staff:
            return Response({
                'error': 'Only admin users can access platform analytics'
            }, status=status.HTTP_403_FORBIDDEN)
        
        period = request.query_params.get('period', '30d')
        
        if period == '7d':
            days = 7
        elif period == '30d':
            days = 30
        elif period == '90d':
            days = 90
        else:
            days = 30
        
        start_date = timezone.now() - timedelta(days=days)
        
        # Calculate platform metrics
        analytics_data = self._calculate_platform_analytics(start_date, days)
        
        return Response(analytics_data)
    
    def _calculate_platform_analytics(self, start_date, days):
        """Calculate comprehensive platform analytics"""
        
        # Basic metrics
        total_revenue = Order.objects.filter(
            created_at__gte=start_date,
            status__in=['delivered', 'shipped', 'processing']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        total_orders = Order.objects.filter(
            created_at__gte=start_date
        ).count()
        
        total_users = User.objects.filter(
            date_joined__gte=start_date
        ).count()
        
        total_books = Book.objects.filter(
            created_at__gte=start_date,
            is_published=True
        ).count()
        
        active_sellers = User.objects.filter(
            role='seller',
            books__isnull=False
        ).distinct().count()
        
        active_affiliates = Affiliate.objects.filter(
            status='approved',
            is_active=True
        ).count()
        
        # Growth calculations
        previous_start_date = start_date - timedelta(days=days)
        previous_revenue = Order.objects.filter(
            created_at__range=[previous_start_date, start_date],
            status__in=['delivered', 'shipped', 'processing']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        previous_orders = Order.objects.filter(
            created_at__range=[previous_start_date, start_date]
        ).count()
        
        previous_users = User.objects.filter(
            date_joined__range=[previous_start_date, start_date]
        ).count()
        
        # Calculate growth percentages
        revenue_growth = self._calculate_growth(total_revenue, previous_revenue)
        order_growth = self._calculate_growth(total_orders, previous_orders)
        user_growth = self._calculate_growth(total_users, previous_users)
        
        # Conversion rate
        total_sessions = 10000  # This would come from actual analytics
        if total_sessions > 0:
            conversion_rate = (total_orders / total_sessions) * 100
        else:
            conversion_rate = 0
        
        # Average order value
        if total_orders > 0:
            average_order_value = total_revenue / total_orders
        else:
            average_order_value = 0
        
        # Top selling categories
        top_categories = Category.objects.filter(
            book__orderitem__order__created_at__gte=start_date
        ).annotate(
            sales=Count('book__orderitem'),
            revenue=Sum('book__orderitem__total_price')
        ).order_by('-revenue')[:5]
        
        top_categories_data = []
        for category in top_categories:
            top_categories_data.append({
                'category': category.name,
                'sales': category.sales,
                'revenue': float(category.revenue or 0)
            })
        
        # Revenue by period
        revenue_by_period = self._get_revenue_by_period(start_date, days)
        
        return {
            'total_revenue': float(total_revenue),
            'revenue_growth': round(revenue_growth, 1),
            'total_orders': total_orders,
            'order_growth': round(order_growth, 1),
            'total_users': total_users,
            'user_growth': round(user_growth, 1),
            'total_books': total_books,
            'active_sellers': active_sellers,
            'active_affiliates': active_affiliates,
            'conversion_rate': round(conversion_rate, 1),
            'average_order_value': round(float(average_order_value), 2),
            'top_selling_categories': top_categories_data,
            'revenue_by_period': revenue_by_period
        }
    
    def _calculate_growth(self, current, previous):
        """Calculate growth percentage"""
        if previous > 0:
            return ((current - previous) / previous) * 100
        elif current > 0:
            return 100.0
        else:
            return 0.0
    
    def _get_revenue_by_period(self, start_date, days):
        """Get revenue broken down by period"""
        revenue_by_period = []
        
        for i in range(days, 0, -1):
            date = timezone.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            daily_revenue = Order.objects.filter(
                created_at__date=date.date(),
                status__in=['delivered', 'shipped', 'processing']
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            revenue_by_period.append({
                'date': date_str,
                'revenue': float(daily_revenue)
            })
        
        return revenue_by_period

class UserManagementView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({
                'error': 'Only admin users can access user management'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get query parameters
        role = request.query_params.get('role')
        is_active = request.query_params.get('is_active')
        search = request.query_params.get('search')
        
        users = User.objects.all().order_by('-date_joined')
        
        # Apply filters
        if role:
            users = users.filter(role=role)
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            users = users.filter(is_active=is_active_bool)
        
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        # Paginate
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_users = users[start_idx:end_idx]
        
        from accounts.serializers import UserSerializer
        serializer = UserSerializer(paginated_users, many=True)
        
        return Response({
            'count': users.count(),
            'results': serializer.data
        })

class ContentModerationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({
                'error': 'Only admin users can access content moderation'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get pending reviews for moderation
        pending_reviews = Review.objects.filter(is_approved=False).count()
        
        # Get reported reviews
        from reviews.models import ReviewReport
        reported_reviews = ReviewReport.objects.filter(is_resolved=False).count()
        
        # Get pending affiliate applications
        pending_affiliates = Affiliate.objects.filter(status='pending').count()
        
        # Get books pending approval
        pending_books = Book.objects.filter(is_published=False).count()
        
        return Response({
            'pending_reviews': pending_reviews,
            'reported_reviews': reported_reviews,
            'pending_affiliates': pending_affiliates,
            'pending_books': pending_books
        })

class SystemHealthView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({
                'error': 'Only admin users can access system health'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Basic system health metrics
        total_users = User.objects.count()
        total_books = Book.objects.count()
        total_orders = Order.objects.count()
        total_reviews = Review.objects.count()
        
        # Recent activity
        last_24_hours = timezone.now() - timedelta(hours=24)
        new_users_24h = User.objects.filter(date_joined__gte=last_24_hours).count()
        new_orders_24h = Order.objects.filter(created_at__gte=last_24_hours).count()
        new_reviews_24h = Review.objects.filter(created_at__gte=last_24_hours).count()
        
        # Performance metrics (simplified)
        avg_response_time = 150  # ms - this would come from actual monitoring
        error_rate = 0.5  # percentage - this would come from actual monitoring
        uptime = 99.9  # percentage
        
        return Response({
            'overview': {
                'total_users': total_users,
                'total_books': total_books,
                'total_orders': total_orders,
                'total_reviews': total_reviews
            },
            'recent_activity': {
                'new_users_24h': new_users_24h,
                'new_orders_24h': new_orders_24h,
                'new_reviews_24h': new_reviews_24h
            },
            'performance': {
                'avg_response_time': avg_response_time,
                'error_rate': error_rate,
                'uptime': uptime
            }
        })