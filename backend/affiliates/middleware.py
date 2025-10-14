from django.utils.deprecation import MiddlewareMixin
from .models import Referral, Affiliate
import urllib.parse

class ReferralTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check for referral parameter in URL
        ref_code = request.GET.get('ref')
        campaign = request.GET.get('campaign')
        
        if ref_code and request.user.is_authenticated:
            try:
                affiliate = Affiliate.objects.get(referral_code=ref_code, status='approved')
                
                # Create or update referral
                referral, created = Referral.objects.get_or_create(
                    affiliate=affiliate,
                    user=request.user,
                    defaults={
                        'ip_address': self.get_client_ip(request),
                        'user_agent': request.META.get('HTTP_USER_AGENT', '')
                    }
                )
                
                # Update referral link clicks if campaign provided
                if campaign and hasattr(affiliate, 'referral_links'):
                    referral_link = affiliate.referral_links.filter(campaign=campaign).first()
                    if referral_link:
                        referral_link.clicks += 1
                        referral_link.save()
                        referral.referral_link = referral_link
                
                referral.save()
                
            except Affiliate.DoesNotExist:
                pass
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip