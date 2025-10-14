import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnc_books.settings')
django.setup()

from orders.models import ShippingMethod

def create_shipping_methods():
    shipping_methods = [
        {
            'name': 'Standard Shipping',
            'price': 4.99,
            'delivery_days': '5-7 business days',
            'is_active': True
        },
        {
            'name': 'Express Shipping',
            'price': 9.99,
            'delivery_days': '2-3 business days',
            'is_active': True
        },
        {
            'name': 'Next Day Delivery',
            'price': 19.99,
            'delivery_days': '1 business day',
            'is_active': True
        },
        {
            'name': 'Free Shipping',
            'price': 0.00,
            'delivery_days': '7-10 business days',
            'is_active': True
        }
    ]
    
    for method_data in shipping_methods:
        method, created = ShippingMethod.objects.get_or_create(
            name=method_data['name'],
            defaults=method_data
        )
        if created:
            print(f"Created shipping method: {method.name}")
    
    print("Shipping methods created successfully!")

if __name__ == '__main__':
    create_shipping_methods()