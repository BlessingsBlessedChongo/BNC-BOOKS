from django.urls import path
from . import views

# Import admin views directly
from .admin_views import PlatformAnalyticsView, UserManagementView, ContentModerationView, SystemHealthView

urlpatterns = [
    # Seller analytics
    path('seller/analytics/', views.SellerAnalyticsView.as_view(), name='seller-analytics'),
    path('seller/dashboard/', views.SellerDashboardView.as_view(), name='seller-dashboard'),
    path('seller/orders/', views.SellerOrdersView.as_view(), name='seller-orders'),
    path('seller/orders/<int:order_id>/', views.SellerOrdersView.as_view(), name='seller-order-detail'),
    path('seller/performance/', views.BookPerformanceView.as_view(), name='book-performance'),
    path('seller/alerts/', views.InventoryAlertsView.as_view(), name='inventory-alerts'),
    path('seller/alerts/<int:alert_id>/resolve/', views.InventoryAlertsView.as_view(), name='resolve-alert'),
    path('seller/reports/generate/', views.GenerateSalesReportView.as_view(), name='generate-sales-report'),
    
    # Admin endpoints
    path('platform/', PlatformAnalyticsView.as_view(), name='platform-analytics'),
    path('admin/users/', UserManagementView.as_view(), name='user-management'),
    path('admin/moderation/', ContentModerationView.as_view(), name='content-moderation'),
    path('admin/health/', SystemHealthView.as_view(), name='system-health'),
]