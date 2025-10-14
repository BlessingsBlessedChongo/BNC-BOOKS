from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal  # ADD THIS IMPORT
import re

def validate_isbn(value):
    """Validate ISBN-10 or ISBN-13 format"""
    # Remove any hyphens or spaces
    isbn = value.replace('-', '').replace(' ', '')
    
    # Check if it's ISBN-10 or ISBN-13
    if len(isbn) == 10:
        # Validate ISBN-10
        if not re.match(r'^\d{9}[\dX]$', isbn):
            raise ValidationError('Invalid ISBN-10 format.')
    elif len(isbn) == 13:
        # Validate ISBN-13
        if not re.match(r'^\d{13}$', isbn):
            raise ValidationError('Invalid ISBN-13 format.')
    else:
        raise ValidationError('ISBN must be 10 or 13 digits long.')

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Book(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('acceptable', 'Acceptable'),
    ]
    
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('spanish', 'Spanish'),
        ('french', 'French'),
        ('german', 'German'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=17, validators=[validate_isbn], unique=True)
    description = models.TextField()
    
    # Pricing & Inventory
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]  # FIXED
    )
    original_price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],  # FIXED
        null=True, 
        blank=True
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    genres = models.ManyToManyField(Genre)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    
    # Publication Details
    pages = models.PositiveIntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=100)
    publication_date = models.DateField()
    
    # Physical Details
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    dimensions = models.CharField(max_length=50, blank=True)
    weight = models.PositiveIntegerField(help_text="Weight in grams", null=True, blank=True)
    
    # Media
    cover_image = models.ImageField(upload_to='book_covers/')
    additional_images = models.JSONField(default=list, blank=True)  # Store list of image URLs
    
    # Status & Features
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Analytics
    total_sales = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]  # FIXED
    )
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('5'))]  # FIXED
    )
    review_count = models.PositiveIntegerField(default=0)
    
    # Relationships
    seller = models.ForeignKey('accounts.User', on_delete=models.CASCADE, limit_choices_to={'role': 'seller'})
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['category']),
            models.Index(fields=['is_published', 'is_featured']),
            models.Index(fields=['price']),
            models.Index(fields=['average_rating']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def clean(self):
        if self.original_price and self.original_price <= self.price:
            raise ValidationError('Original price must be greater than current price if provided.')
    
    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100, 1)
        return 0