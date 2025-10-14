import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnc_books.settings')
django.setup()

from accounts.models import User
from books.models import Category, Genre

def create_test_data():
    # Create categories
    categories = [
        "Fiction", "Non-Fiction", "Science", "Technology", 
        "Business", "Self-Help", "Biography", "History", 
        "Children", "Young Adult"
    ]
    
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)
        print(f"Created category: {category_name}")
    
    # Create genres
    genres = [
        "Fantasy", "Science Fiction", "Mystery", "Romance",
        "Thriller", "Horror", "Adventure", "Historical",
        "Contemporary", "Dystopian"
    ]
    
    for genre_name in genres:
        Genre.objects.get_or_create(name=genre_name)
        print(f"Created genre: {genre_name}")
    
    print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data()