import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnc_books.settings')
django.setup()

from accounts.models import User
from affiliates.models import Affiliate, ReferralLink, Commission
from orders.models import Order
from datetime import datetime, timedelta

def create_test_affiliates():
    # Create affiliate user
    affiliate_user, created = User.objects.get_or_create(
        email='affiliate@example.com',
        defaults={
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'role': 'affiliate'
        }
    )
    if created:
        affiliate_user.set_password('AffiliatePassword123!')
        affiliate_user.save()
        print("Created affiliate user")
    
    # Create affiliate account
    affiliate, created = Affiliate.objects.get_or_create(
        user=affiliate_user,
        defaults={
            'status': 'approved',
            'commission_rate': 10.00,
            'paypal_email': 'affiliate@example.com',
            'preferred_payment_method': 'paypal',
            'total_earnings': 1250.50,
            'paid_earnings': 400.00,
            'pending_earnings': 850.50
        }
    )
    
    if created:
        print("Created affiliate account")
    
    # Create sample referral links
    referral_links_data = [
        {
            'campaign': 'summer_sale_2024',
            'clicks': 1500,
            'conversions': 25
        },
        {
            'campaign': 'winter_promo',
            'clicks': 800,
            'conversions': 15
        }
    ]
    
    for link_data in referral_links_data:
        link, created = ReferralLink.objects.get_or_create(
            affiliate=affiliate,
            campaign=link_data['campaign'],
            defaults={
                'url': f"http://localhost:3000/ref/{affiliate.referral_code}?campaign={link_data['campaign']}",
                'clicks': link_data['clicks'],
                'conversions': link_data['conversions']
            }
        )
        if created:
            print(f"Created referral link: {link.campaign}")
    
    # Create sample commissions
    commissions_data = [
        {
            'amount': 12.99,
            'commission_rate': 10.0,
            'type': 'sale',
            'status': 'pending',
            'description': 'Commission from book sale',
            'calculated_on': 129.90,
            'created_at': datetime.now() - timedelta(days=2)
        },
        {
            'amount': 25.50,
            'commission_rate': 10.0,
            'type': 'sale',
            'status': 'approved',
            'description': 'Commission from multiple book sales',
            'calculated_on': 255.00,
            'created_at': datetime.now() - timedelta(days=5)
        },
        {
            'amount': 8.75,
            'commission_rate': 10.0,
            'type': 'sale',
            'status': 'paid',
            'description': 'Commission from ebook sale',
            'calculated_on': 87.50,
            'created_at': datetime.now() - timedelta(days=10)
        }
    ]
    
    for commission_data in commissions_data:
        created_at = commission_data.pop('created_at')
        commission = Commission.objects.create(
            affiliate=affiliate,
            **commission_data
        )
        commission.created_at = created_at
        commission.save()
        print(f"Created commission: ${commission.amount}")
    
    print("Test affiliates created successfully!")

if __name__ == '__main__':
    create_test_affiliates()