from django.urls import path
from . import views

urlpatterns = [
    # Cart endpoints
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/items/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/items/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/items/<int:item_id>/remove/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/clear/', views.ClearCartView.as_view(), name='clear-cart'),
    
    # Order endpoints
    path('', views.UserOrdersView.as_view(), name='user-orders'),
    path('create/', views.CreateOrderView.as_view(), name='create-order'),
    path('shipping-methods/', views.ShippingMethodsView.as_view(), name='shipping-methods'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/cancel/', views.CancelOrderView.as_view(), name='cancel-order'),
    path('<int:order_id>/return/', views.RequestReturnView.as_view(), name='request-return'),
]