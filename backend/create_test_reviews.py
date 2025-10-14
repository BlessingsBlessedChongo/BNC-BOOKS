import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnc_books.settings')
django.setup()

from accounts.models import User
from books.models import Book
from reviews.models import Review

def create_test_reviews():
    # Get or create a buyer user
    buyer, created = User.objects.get_or_create(
        email='buyer@example.com',
        defaults={
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'buyer'
        }
    )
    if created:
        buyer.set_password('BuyerPassword123!')
        buyer.save()
        print("Created buyer user")
    
    # Get books
    harry_potter = Book.objects.get(title__icontains="Harry Potter")
    hobbit = Book.objects.get(title__icontains="Hobbit")
    catcher = Book.objects.get(title__icontains="Catcher")
    
    # Create sample reviews
    reviews_data = [
        {
            'user': buyer,
            'book': harry_potter,
            'rating': 5,
            'title': "Amazing book!",
            'comment': "One of the best books I've ever read. Highly recommended!",
            'pros': "Engaging plot, well-developed characters",
            'cons': "A bit long in some parts",
            'would_recommend': True,
            'verified_purchase': True,
            'helpful_count': 25,
            'not_helpful_count': 2,
            'created_at': datetime.now() - timedelta(days=10)
        },
        {
            'user': buyer,
            'book': hobbit,
            'rating': 4,
            'title': "Great fantasy adventure",
            'comment': "A wonderful journey through Middle-earth. Tolkien's world-building is incredible.",
            'pros': "Rich world-building, memorable characters",
            'cons': "Slow pacing at times",
            'would_recommend': True,
            'verified_purchase': True,
            'helpful_count': 15,
            'not_helpful_count': 1,
            'created_at': datetime.now() - timedelta(days=5)
        },
        {
            'user': buyer,
            'book': catcher,
            'rating': 3,
            'title': "Classic but dated",
            'comment': "An important piece of literature but didn't resonate with me as much as I expected.",
            'pros': "Historical significance, unique narrative voice",
            'cons': "Dated references, unlikeable protagonist",
            'would_recommend': False,
            'verified_purchase': True,
            'helpful_count': 8,
            'not_helpful_count': 3,
            'created_at': datetime.now() - timedelta(days=2)
        }
    ]
    
    for review_data in reviews_data:
        # Remove created_at for the object creation
        created_at = review_data.pop('created_at')
        
        review, created = Review.objects.get_or_create(
            user=review_data['user'],
            book=review_data['book'],
            defaults=review_data
        )
        
        if created:
            # Set the created_at timestamp
            review.created_at = created_at
            review.save()
            print(f"Created review: {review.title}")
    
    print("Test reviews created successfully!")

if __name__ == '__main__':
    create_test_reviews()