from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import Cart, CartItem, Order, OrderItem, ShippingMethod
from .serializers import (
    CartSerializer, AddToCartSerializer, UpdateCartItemSerializer,
    OrderSerializer, OrderDetailSerializer, CreateOrderSerializer,
    ShippingMethodSerializer, ReturnRequestSerializer
)

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        book = serializer.validated_data['book']
        quantity = serializer.validated_data['quantity']
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item exists
            cart_item.quantity += quantity
            cart_item.save()
        
        # Serialize the response
        response_serializer = CartSerializer(cart_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(
                pk=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UpdateCartItemSerializer(
            cart_item, 
            data=request.data, 
            partial=True
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check stock availability
        new_quantity = serializer.validated_data.get('quantity', cart_item.quantity)
        if new_quantity > cart_item.book.stock_quantity:
            return Response({
                'quantity': [
                    f"Requested quantity ({new_quantity}) exceeds available stock ({cart_item.book.stock_quantity})"
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        # Return updated cart item
        cart_serializer = CartSerializer(cart_item)
        return Response(cart_serializer.data)

class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(
                pk=item_id,
                cart__user=request.user
            )
            cart_item.delete()
            
            return Response({
                'message': 'Item removed from cart successfully'
            }, status=status.HTTP_200_OK)
            
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        
        return Response({
            'message': 'Cart cleared successfully'
        }, status=status.HTTP_200_OK)

class ShippingMethodsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        shipping_methods = ShippingMethod.objects.filter(is_active=True)
        serializer = ShippingMethodSerializer(shipping_methods, many=True)
        return Response(serializer.data)

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if cart.items.count() == 0:
            return Response(
                {'error': 'Cart is empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate cart items stock
        for cart_item in cart.items.all():
            if cart_item.quantity > cart_item.book.stock_quantity:
                return Response({
                    'error': f"Not enough stock for {cart_item.book.title}. Available: {cart_item.book.stock_quantity}, Requested: {cart_item.quantity}"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        shipping_method = data['shipping_method_id']
        
        # Calculate totals
        subtotal = cart.subtotal
        shipping_cost = shipping_method.price
        tax_amount = subtotal * 0.1  # 10% tax for example
        total_amount = subtotal + shipping_cost + tax_amount
        
        # Handle billing address
        if data['billing_same_as_shipping']:
            billing_address = data['shipping_address']
        else:
            billing_address = data['billing_address']
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=data['shipping_address'],
            billing_address=billing_address,
            shipping_method=shipping_method,
            payment_method=data['payment_method'],
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            total_amount=total_amount
        )
        
        # Create order items and update book stock
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                unit_price=cart_item.book.price,
                total_price=cart_item.total_price
            )
            
            # Update book stock
            cart_item.book.stock_quantity -= cart_item.quantity
            cart_item.book.total_sales += cart_item.quantity
            cart_item.book.total_revenue += cart_item.total_price
            cart_item.book.save()
        
        # Clear the cart
        cart.items.all().delete()
        
        # Serialize response
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

class UserOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only pending orders can be cancelled
        if order.status != 'pending':
            return Response({
                'error': 'Only pending orders can be cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Restore book stock
        for order_item in order.items.all():
            book = order_item.book
            book.stock_quantity += order_item.quantity
            book.total_sales -= order_item.quantity
            book.total_revenue -= order_item.total_price
            book.save()
        
        # Update order status
        order.status = 'cancelled'
        order.cancelled_at = timezone.now()
        order.save()
        
        return Response({
            'id': order.id,
            'status': order.status,
            'cancelled_at': order.cancelled_at.isoformat()
        })

class RequestReturnView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only delivered orders can be returned
        if order.status != 'delivered':
            return Response({
                'error': 'Only delivered orders can be returned'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ReturnRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create return request (simplified - full implementation in next batch)
        data = serializer.validated_data
        
        return Response({
            'message': 'Return request submitted successfully',
            'reason': data['reason'],
            'comments': data.get('comments', '')
        }, status=status.HTTP_200_OK)