from django.contrib import admin
from .models import Category, Genre, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    # REMOVE prepopulated_fields since we don't have a slug field

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    # REMOVE prepopulated_fields since we don't have a slug field

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock_quantity', 'is_published', 'is_featured', 'seller')
    list_filter = ('category', 'is_published', 'is_featured', 'condition', 'language')
    search_fields = ('title', 'author', 'isbn', 'description')
    readonly_fields = ('total_sales', 'total_revenue', 'average_rating', 'review_count', 'created_at', 'updated_at')
    list_editable = ('price', 'stock_quantity', 'is_published', 'is_featured')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'original_price', 'stock_quantity')
        }),
        ('Categorization', {
            'fields': ('category', 'genres', 'language')
        }),
        ('Publication Details', {
            'fields': ('pages', 'publisher', 'publication_date')
        }),
        ('Physical Details', {
            'fields': ('condition', 'dimensions', 'weight')
        }),
        ('Media', {
            'fields': ('cover_image', 'additional_images')
        }),
        ('Status & Features', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Analytics', {
            'fields': ('total_sales', 'total_revenue', 'average_rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('seller',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )