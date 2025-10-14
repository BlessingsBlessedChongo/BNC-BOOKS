from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod, ReturnRequest

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'subtotal', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity', 'total_price')
    list_filter = ('cart__user',)

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'delivery_days', 'is_active')
    list_editable = ('price', 'is_active')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('unit_price', 'total_price')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_method')
        }),
        ('Addresses', {
            'fields': ('shipping_address', 'billing_address')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total_amount')
        }),
        ('Shipping', {
            'fields': ('shipping_method',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processing_at', 
                      'shipped_at', 'delivered_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'unit_price', 'total_price')
    list_filter = ('order__status',)

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('order', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason')
    readonly_fields = ('created_at', 'updated_at')