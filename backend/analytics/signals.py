from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from orders.models import Order, OrderItem
from books.models import Book
from .models import BookPerformance, DailySales, InventoryAlert

@receiver(post_save, sender=OrderItem)
def update_book_performance_on_order(sender, instance, created, **kwargs):
    """Update book performance when an order item is created"""
    if created and instance.order.status in ['processing', 'shipped', 'delivered']:
        performance, created = BookPerformance.objects.get_or_create(book=instance.book)
        performance.purchases += instance.quantity
        performance.revenue += instance.total_price
        
        # Recalculate conversion rate
        if performance.views > 0:
            performance.conversion_rate = (performance.purchases / performance.views) * 100
        
        performance.save()

@receiver(post_save, sender=Book)
def check_inventory_on_book_save(sender, instance, **kwargs):
    """Check inventory levels and create alerts"""
    from .models import InventoryAlert
    
    # Remove resolved alerts if stock is replenished
    if instance.stock_quantity > 10:
        InventoryAlert.objects.filter(
            book=instance,
            alert_type__in=['low_stock', 'out_of_stock'],
            is_resolved=False
        ).update(is_resolved=True, resolved_at=timezone.now())
    
    # Create low stock alert
    elif instance.stock_quantity <= 10 and instance.stock_quantity > 0:
        alert, created = InventoryAlert.objects.get_or_create(
            seller=instance.seller,
            book=instance,
            alert_type='low_stock',
            is_resolved=False,
            defaults={
                'priority': 'high' if instance.stock_quantity <= 3 else 'medium',
                'message': f'Low stock: Only {instance.stock_quantity} units left',
                'current_stock': instance.stock_quantity,
                'threshold': 10
            }
        )
    
    # Create out of stock alert
    elif instance.stock_quantity == 0:
        alert, created = InventoryAlert.objects.get_or_create(
            seller=instance.seller,
            book=instance,
            alert_type='out_of_stock',
            is_resolved=False,
            defaults={
                'priority': 'high',
                'message': 'Out of stock: 0 units in inventory',
                'current_stock': 0,
                'threshold': 1
            }
        )