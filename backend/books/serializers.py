from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Book, Category, Genre
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'description')

class BookListSerializer(serializers.ModelSerializer):
    seller_store = serializers.CharField(source='seller.profile.store_name', read_only=True)
    
    class Meta:
        model = Book
        fields = (
            'id', 'title', 'author', 'isbn', 'price', 'original_price',
            'stock_quantity', 'category', 'genres', 'cover_image',
            'average_rating', 'review_count', 'is_featured', 'seller_store'
        )

class BookDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = (
            'id', 'title', 'author', 'isbn', 'description', 'price', 'original_price',
            'stock_quantity', 'category', 'category_name', 'genres', 'language', 'pages',
            'publisher', 'publication_date', 'condition', 'cover_image', 'additional_images',
            'dimensions', 'weight', 'is_published', 'is_featured', 'average_rating',
            'review_count', 'total_sales', 'total_revenue', 'discount_percentage',
            'seller', 'created_at', 'updated_at'
        )
        read_only_fields = ('total_sales', 'total_revenue', 'average_rating', 'review_count')
    
    def get_seller(self, obj):
        return {
            'id': obj.seller.id,
            'store_name': getattr(obj.seller.profile, 'store_name', ''),
            'user': {
                'id': obj.seller.id,
                'first_name': obj.seller.first_name,
                'last_name': obj.seller.last_name
            }
        }

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'title', 'author', 'isbn', 'description', 'price', 'original_price',
            'stock_quantity', 'category', 'genres', 'language', 'pages',
            'publisher', 'publication_date', 'condition', 'cover_image',
            'dimensions', 'weight', 'is_published', 'is_featured'
        )
    
    def validate_title(self, value):
        if len(value) < 2 or len(value) > 200:
            raise serializers.ValidationError("Title must be between 2 and 200 characters.")
        return value
    
    def validate_author(self, value):
        if len(value) < 2 or len(value) > 100:
            raise serializers.ValidationError("Author name must be between 2 and 100 characters.")
        return value
    
    def validate_price(self, value):
        if value <= 0 or value > 9999.99:
            raise serializers.ValidationError("Price must be between 0.01 and 9999.99.")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0 or value > 999999:
            raise serializers.ValidationError("Stock quantity must be between 0 and 999999.")
        return value
    
    def validate(self, data):
        if data.get('original_price') and data['original_price'] <= data['price']:
            raise serializers.ValidationError({
                'original_price': 'Original price must be greater than current price if provided.'
            })
        return data
    
    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)

class InventoryUpdateSerializer(serializers.Serializer):
    stock_quantity = serializers.IntegerField(
        required=True,
        min_value=0,
        max_value=999999
    )
    adjustment_type = serializers.ChoiceField(
        choices=[('set', 'Set'), ('add', 'Add'), ('subtract', 'Subtract')],
        required=False,
        default='set'
    )
    adjustment_amount = serializers.IntegerField(required=False, min_value=0)
    reason = serializers.CharField(required=False, max_length=100)
    notes = serializers.CharField(required=False, max_length=500)
    
    def validate(self, data):
        if data.get('adjustment_type') in ['add', 'subtract'] and not data.get('adjustment_amount'):
            raise serializers.ValidationError({
                'adjustment_amount': 'Adjustment amount is required for add/subtract operations.'
            })
        return data