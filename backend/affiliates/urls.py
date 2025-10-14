from django.urls import path
from . import views

urlpatterns = [
    # Affiliate registration
    path('register/', views.AffiliateRegistrationView.as_view(), name='affiliate-register'),
    
    # Referral links
    path('referral-links/', views.GenerateReferralLinkView.as_view(), name='generate-referral-link'),
    
    # Commissions
    path('commissions/', views.GetCommissionsView.as_view(), name='affiliate-commissions'),
    
    # Payouts
    path('payouts/', views.RequestPayoutView.as_view(), name='request-payout'),
    
    # Analytics
    path('analytics/', views.AffiliateAnalyticsView.as_view(), name='affiliate-analytics'),
    
    # Dashboard
    path('dashboard/', views.AffiliateDashboardView.as_view(), name='affiliate-dashboard'),
]