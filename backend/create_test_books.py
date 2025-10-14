import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnc_books.settings')
django.setup()

from accounts.models import User
from books.models import Book, Category, Genre

def create_test_books():
    # Get or create a seller user
    seller, created = User.objects.get_or_create(
        email='seller@example.com',
        defaults={
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'role': 'seller'
        }
    )
    if created:
        seller.set_password('SellerPassword123!')
        seller.save()
        seller.profile.store_name = "Magic Books Emporium"
        seller.profile.save()
        print("Created seller user")
    
    # Get categories and genres
    fiction_category = Category.objects.get(name='Fiction')
    fantasy_genre = Genre.objects.get(name='Fantasy')
    young_adult_genre = Genre.objects.get(name='Young Adult')
    
    # Create sample books
    books_data = [
        {
            'title': "Harry Potter and the Philosopher's Stone",
            'author': "J.K. Rowling",
            'isbn': "9780439708180",
            'description': "Harry Potter has never even heard of Hogwarts when the letters start dropping on the doormat at number four, Privet Drive.",
            'price': 12.99,
            'original_price': 15.99,
            'stock_quantity': 50,
            'category': fiction_category,
            'genres': [fantasy_genre, young_adult_genre],
            'language': 'english',
            'pages': 320,
            'publisher': 'Bloomsbury',
            'publication_date': date(1997, 6, 26),
            'condition': 'new',
            'is_published': True,
            'is_featured': True,
            'average_rating': 4.8,
            'review_count': 150,
            'total_sales': 500,
            'total_revenue': 6495.00,
            'dimensions': "7.6 x 5.3 x 1.2 inches",
            'weight': 300,
        },
        {
            'title': "The Hobbit",
            'author': "J.R.R. Tolkien",
            'isbn': "9780547928227",
            'description': "Bilbo Baggins is a hobbit who enjoys a comfortable, unambitious life.",
            'price': 14.99,
            'original_price': 18.99,
            'stock_quantity': 30,
            'category': fiction_category,
            'genres': [fantasy_genre],
            'language': 'english',
            'pages': 300,
            'publisher': 'Houghton Mifflin',
            'publication_date': date(1937, 9, 21),
            'condition': 'new',
            'is_published': True,
            'is_featured': False,
            'average_rating': 4.7,
            'review_count': 89,
            'total_sales': 200,
            'total_revenue': 2998.00,
        },
        {
            'title': "The Catcher in the Rye",
            'author': "J.D. Salinger",
            'isbn': "9780316769174",
            'description': "The hero-narrator of The Catcher in the Rye is an ancient child of sixteen.",
            'price': 10.99,
            'stock_quantity': 25,
            'category': fiction_category,
            'genres': [Genre.objects.get(name='Contemporary')],
            'language': 'english',
            'pages': 234,
            'publisher': 'Little, Brown and Company',
            'publication_date': date(1951, 7, 16),
            'condition': 'like_new',
            'is_published': True,
            'is_featured': True,
            'average_rating': 4.0,
            'review_count': 45,
            'total_sales': 120,
            'total_revenue': 1318.80,
        }
    ]
    
    for book_data in books_data:
        genres = book_data.pop('genres')
        book, created = Book.objects.get_or_create(
            isbn=book_data['isbn'],
            defaults=book_data
        )
        if created:
            book.seller = seller
            book.genres.set(genres)
            book.save()
            print(f"Created book: {book.title}")
    
    print("Test books created successfully!")

if __name__ == '__main__':
    create_test_books()