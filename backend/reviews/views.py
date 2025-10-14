from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from django.utils import timezone
from .models import Review, ReviewVote, ReviewReport
from books.models import Book
from orders.models import OrderItem
from .serializers import (
    ReviewSerializer, CreateReviewSerializer, UpdateReviewSerializer,
    ReviewVoteSerializer, ReviewReportSerializer, CanReviewSerializer,
    ReviewSummarySerializer
)

class CreateReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CreateReviewSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user can review this book
        can_review, reason = self._can_user_review(request.user, serializer.validated_data['book'])
        if not can_review:
            return Response({
                'error': reason
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the review
        review = serializer.save(user=request.user)
        
        # Serialize response
        response_serializer = ReviewSerializer(review)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def _can_user_review(self, user, book):
        """Check if user can review the book"""
        # Check if user has already reviewed
        if Review.objects.filter(user=user, book=book).exists():
            return False, "You have already reviewed this book."
        
        # Check if user has purchased the book
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            order__status='delivered',
            book=book
        ).exists()
        
        if not has_purchased:
            return False, "You haven't purchased this book yet"
        
        return True, None

class BookReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        book_id = self.request.query_params.get('book')
        if book_id:
            return Review.objects.filter(
                book_id=book_id, 
                is_approved=True
            ).select_related('user', 'book')
        return Review.objects.filter(is_approved=True).select_related('user', 'book')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add count to response
        book_id = request.query_params.get('book')
        if book_id:
            count = Review.objects.filter(book_id=book_id, is_approved=True).count()
        else:
            count = Review.objects.filter(is_approved=True).count()
        
        response.data = {
            'count': count,
            'results': response.data
        }
        
        return response

class UserReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('book')

class ReviewDetailView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateReviewSerializer
        return ReviewSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        # Return full review data
        full_serializer = ReviewSerializer(instance)
        return Response(full_serializer.data)

class CanReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user has already reviewed
        already_reviewed = Review.objects.filter(user=request.user, book=book).exists()
        
        # Check if user has purchased the book
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status='delivered',
            book=book
        ).exists()
        
        can_review = has_purchased and not already_reviewed
        
        if not can_review:
            if already_reviewed:
                reason = "You have already reviewed this book."
            elif not has_purchased:
                reason = "You haven't purchased this book yet"
            else:
                reason = "Unable to review this book."
        else:
            reason = None
        
        serializer = CanReviewSerializer({
            'can_review': can_review,
            'reason': reason,
            'purchased_book': has_purchased
        })
        
        return Response(serializer.data)

class ReviewVoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id, is_approved=True)
        except Review.DoesNotExist:
            return Response(
                {'error': 'Review not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        vote_type = request.data.get('vote_type')
        
        if vote_type not in ['helpful', 'not_helpful']:
            return Response({
                'error': 'Vote type must be "helpful" or "not_helpful"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has already voted
        existing_vote = ReviewVote.objects.filter(
            user=request.user, 
            review=review
        ).first()
        
        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # Remove the vote if clicking the same button
                existing_vote.delete()
                
                # Update counts
                if vote_type == 'helpful':
                    review.helpful_count = max(0, review.helpful_count - 1)
                else:
                    review.not_helpful_count = max(0, review.not_helpful_count - 1)
            else:
                # Change vote type
                if existing_vote.vote_type == 'helpful':
                    review.helpful_count = max(0, review.helpful_count - 1)
                    review.not_helpful_count += 1
                else:
                    review.not_helpful_count = max(0, review.not_helpful_count - 1)
                    review.helpful_count += 1
                
                existing_vote.vote_type = vote_type
                existing_vote.save()
        else:
            # Create new vote
            ReviewVote.objects.create(
                user=request.user,
                review=review,
                vote_type=vote_type
            )
            
            # Update counts
            if vote_type == 'helpful':
                review.helpful_count += 1
            else:
                review.not_helpful_count += 1
        
        review.save()
        
        return Response({
            'helpful_count': review.helpful_count,
            'not_helpful_count': review.not_helpful_count,
            'user_vote': vote_type if not existing_vote or existing_vote.vote_type == vote_type else None
        })

class ReviewReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id, is_approved=True)
        except Review.DoesNotExist:
            return Response(
                {'error': 'Review not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user has already reported this review
        if ReviewReport.objects.filter(user=request.user, review=review).exists():
            return Response({
                'error': 'You have already reported this review'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ReviewReportSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        report = serializer.save(user=request.user, review=review)
        
        return Response({
            'message': 'Review reported successfully',
            'report_id': report.id
        }, status=status.HTTP_201_CREATED)

class ReviewSummaryView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get review statistics
        reviews = Review.objects.filter(book=book, is_approved=True)
        total_reviews = reviews.count()
        
        if total_reviews == 0:
            return Response({
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                'verified_purchases': 0,
                'would_recommend_percentage': 0
            })
        
        # Calculate rating distribution
        rating_distribution = reviews.values('rating').annotate(
            count=Count('id')
        ).order_by('rating')
        
        distribution_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for item in rating_distribution:
            distribution_dict[item['rating']] = item['count']
        
        # Calculate other statistics
        verified_purchases = reviews.filter(verified_purchase=True).count()
        would_recommend = reviews.filter(would_recommend=True).count()
        would_recommend_percentage = round((would_recommend / total_reviews) * 100, 1)
        
        serializer = ReviewSummarySerializer({
            'total_reviews': total_reviews,
            'average_rating': book.average_rating,
            'rating_distribution': distribution_dict,
            'verified_purchases': verified_purchases,
            'would_recommend_percentage': would_recommend_percentage
        })
        
        return Response(serializer.data)