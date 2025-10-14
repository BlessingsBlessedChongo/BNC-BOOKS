from django.urls import path
from . import views

urlpatterns = [
    # Review endpoints
    path('', views.CreateReviewView.as_view(), name='create-review'),
    path('', views.BookReviewsView.as_view(), name='book-reviews'),
    path('my-reviews/', views.UserReviewsView.as_view(), name='user-reviews'),
    path('can-review/<int:book_id>/', views.CanReviewView.as_view(), name='can-review'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # Review interactions
    path('<int:review_id>/vote/', views.ReviewVoteView.as_view(), name='review-vote'),
    path('<int:review_id>/report/', views.ReviewReportView.as_view(), name='review-report'),
    
    # Analytics
    path('summary/<int:book_id>/', views.ReviewSummaryView.as_view(), name='review-summary'),
]