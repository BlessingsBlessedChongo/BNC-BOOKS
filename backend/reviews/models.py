from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from books.models import Book
from orders.models import Order, OrderItem

class Review(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['book', 'rating']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['verified_purchase']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.book.title} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        # Check if this is a verified purchase before saving
        if not self.pk:  # Only on creation
            self.verified_purchase = self._check_verified_purchase()
        
        super().save(*args, **kwargs)
        
        # Update book's average rating and review count
        self._update_book_ratings()
    
    def _check_verified_purchase(self):
        """Check if the user has purchased this book"""
        return OrderItem.objects.filter(
            order__user=self.user,
            order__status='delivered',
            book=self.book
        ).exists()
    
    def _update_book_ratings(self):
        """Update the book's average rating and review count"""
        reviews = Review.objects.filter(book=self.book, is_approved=True)
        total_reviews = reviews.count()
        
        if total_reviews > 0:
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.book.average_rating = round(avg_rating, 2)
            self.book.review_count = total_reviews
            self.book.save()

class ReviewVote(models.Model):
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'review']
    
    def __str__(self):
        return f"{self.user.email} - {self.vote_type} - {self.review}"

class ReviewReport(models.Model):
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('false_information', 'False Information'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    comments = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'review']
    
    def __str__(self):
        return f"Report by {self.user.email} on {self.review}"