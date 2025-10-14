from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from books.models import Book
from orders.models import Order, OrderItem

class SellerAnalytics(models.Model):
    seller = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='analytics'
    )
    total_revenue = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    total_orders = models.PositiveIntegerField(default=0)
    total_books_sold = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    conversion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0
    )
    average_order_value = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Seller Analytics"
    
    def __str__(self):
        return f"Analytics for {self.seller.email}"

class DailySales(models.Model):
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='daily_sales'
    )
    date = models.DateField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    orders = models.PositiveIntegerField(default=0)
    books_sold = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['seller', 'date']
        ordering = ['-date']
        verbose_name_plural = "Daily Sales"
    
    def __str__(self):
        return f"Sales for {self.seller.email} on {self.date}"

class BookPerformance(models.Model):
    book = models.OneToOneField(
        Book, 
        on_delete=models.CASCADE, 
        related_name='performance'
    )
    views = models.PositiveIntegerField(default=0)
    add_to_cart_count = models.PositiveIntegerField(default=0)
    purchases = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conversion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Performance for {self.book.title}"

class InventoryAlert(models.Model):
    ALERT_TYPES = [
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('overstock', 'Overstock'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='inventory_alerts'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='alerts'
    )
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    message = models.TextField()
    current_stock = models.PositiveIntegerField()
    threshold = models.PositiveIntegerField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type} alert for {self.book.title}"

class SalesReport(models.Model):
    REPORT_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sales_reports'
    )
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_books_sold = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    top_selling_books = models.JSONField(default=list)
    revenue_by_date = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.report_type} report for {self.seller.email}"