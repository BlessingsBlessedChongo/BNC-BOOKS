from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod, ReturnRequest, ReturnItem
from books.serializers import BookListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ('id', 'book', 'quantity', 'total_price', 'added_at')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_items', 'subtotal', 'created_at', 'updated_at')

class AddToCartSerializer(serializers.Serializer):
    book = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_book(self, value):
        from books.models import Book
        try:
            book = Book.objects.get(pk=value, is_published=True)
            return book
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
    
    def validate(self, data):
        book = data['book']
        quantity = data['quantity']
        
        if quantity > book.stock_quantity:
            raise serializers.ValidationError({
                'quantity': [f"Requested quantity ({quantity}) exceeds available stock ({book.stock_quantity})"]
            })
        
        return data

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        
        # Check stock availability in the view since we need the book instance
        return value

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ('id', 'name', 'price', 'delivery_days')

class AddressSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    street_address = serializers.CharField(max_length=255, required=True)
    apartment = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=True)
    state = serializers.CharField(max_length=100, required=True)
    zip_code = serializers.CharField(max_length=20, required=True)
    country = serializers.CharField(max_length=100, default='US')
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'book', 'quantity', 'unit_price', 'total_price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = serializers.JSONField()
    billing_address = serializers.JSONField()
    shipping_method = ShippingMethodSerializer(read_only=True)
    has_reviewed = serializers.SerializerMethodField()
    return_requested = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'user', 'items', 'shipping_address',
            'billing_address', 'shipping_method', 'payment_method',
            'subtotal', 'shipping_cost', 'tax_amount', 'total_amount',
            'status', 'created_at', 'has_reviewed', 'return_requested'
        )
        read_only_fields = ('order_number', 'user', 'subtotal', 'shipping_cost', 
                          'tax_amount', 'total_amount', 'status')
    
    def get_has_reviewed(self, obj):
        # This will be implemented in the reviews batch
        return False
    
    def get_return_requested(self, obj):
        return obj.return_requests.exists()

class OrderDetailSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + (
            'processing_at', 'shipped_at', 'delivered_at', 
            'cancelled_at', 'updated_at'
        )

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = AddressSerializer(required=True)
    billing_address = AddressSerializer(required=False)
    shipping_method_id = serializers.IntegerField(required=True)
    payment_method = serializers.ChoiceField(
        choices=Order.PAYMENT_METHOD_CHOICES,
        required=True
    )
    billing_same_as_shipping = serializers.BooleanField(default=False)
    
    def validate_shipping_method_id(self, value):
        try:
            shipping_method = ShippingMethod.objects.get(pk=value, is_active=True)
            return shipping_method
        except ShippingMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid shipping method")
    
    def validate(self, data):
        if data.get('billing_same_as_shipping') and data.get('billing_address'):
            raise serializers.ValidationError({
                'billing_address': 'Cannot provide billing address when billing_same_as_shipping is True'
            })
        
        if not data.get('billing_same_as_shipping') and not data.get('billing_address'):
            raise serializers.ValidationError({
                'billing_address': 'Billing address is required when billing_same_as_shipping is False'
            })
        
        return data

class ReturnItemSerializer(serializers.Serializer):
    order_item = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    reason = serializers.ChoiceField(choices=ReturnRequest.REASON_CHOICES, required=True)

class ReturnRequestSerializer(serializers.Serializer):
    reason = serializers.ChoiceField(choices=ReturnRequest.REASON_CHOICES, required=True)
    comments = serializers.CharField(required=False, allow_blank=True)
    return_items = ReturnItemSerializer(many=True, required=True)
    
    def validate_return_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one return item is required")
        return value