from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review, ReviewVote, ReviewReport
from accounts.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'user', 'book', 'book_title', 'rating', 'title', 'comment',
            'pros', 'cons', 'would_recommend', 'verified_purchase',
            'helpful_count', 'not_helpful_count', 'is_approved',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'user', 'verified_purchase', 'helpful_count', 
            'not_helpful_count', 'is_approved', 'created_at', 'updated_at'
        )
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
    
    def validate_comment(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long.")
        return value

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'book', 'rating', 'title', 'comment', 'pros', 
            'cons', 'would_recommend'
        )
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        book = data['book']
        
        # Check if user has already reviewed this book
        if Review.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError({
                'book': 'You have already reviewed this book.'
            })
        
        return data

class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'title', 'comment', 'pros', 'cons', 'would_recommend')
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class ReviewVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewVote
        fields = ('id', 'user', 'review', 'vote_type', 'created_at')
        read_only_fields = ('user', 'created_at')

class ReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReport
        fields = ('id', 'user', 'review', 'reason', 'comments', 'created_at')
        read_only_fields = ('user', 'created_at')

class CanReviewSerializer(serializers.Serializer):
    can_review = serializers.BooleanField()
    reason = serializers.CharField(allow_null=True)
    purchased_book = serializers.BooleanField()

class ReviewSummarySerializer(serializers.Serializer):
    total_reviews = serializers.IntegerField()
    average_rating = serializers.FloatField()
    rating_distribution = serializers.DictField()
    verified_purchases = serializers.IntegerField()
    would_recommend_percentage = serializers.FloatField()