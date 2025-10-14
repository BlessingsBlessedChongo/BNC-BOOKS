from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('', views.BookListView.as_view(), name='book-list'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('featured/', views.FeaturedBooksView.as_view(), name='featured-books'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Seller endpoints
    path('seller/books/', views.SellerBookListView.as_view(), name='seller-book-list'),
    path('seller/books/', views.SellerBookCreateView.as_view(), name='seller-book-create'),
    path('seller/books/<int:pk>/', views.SellerBookDetailView.as_view(), name='seller-book-detail'),
    path('seller/books/<int:pk>/inventory/', views.InventoryUpdateView.as_view(), name='inventory-update'),
]