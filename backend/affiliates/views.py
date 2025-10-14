from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, Avg
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import json

from .models import Affiliate, ReferralLink, Referral, Commission, Payout
from .serializers import (
    AffiliateRegistrationSerializer, AffiliateSerializer,
    ReferralLinkSerializer, CreateReferralLinkSerializer,
    CommissionSerializer, PayoutSerializer, CreatePayoutSerializer,
    AffiliateAnalyticsSerializer
)

class AffiliateRegistrationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Check if user is already an affiliate
        if hasattr(request.user, 'affiliate'):
            return Response({
                'error': 'You are already registered as an affiliate'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has the correct role
        if request.user.role != 'affiliate':
            return Response({
                'error': 'Only users with affiliate role can register as affiliates'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AffiliateRegistrationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create affiliate
        affiliate_data = serializer.validated_data.copy()
        bank_account = affiliate_data.pop('bank_account', None)
        
        affiliate = Affiliate.objects.create(
            user=request.user,
            **affiliate_data
        )
        
        if bank_account:
            affiliate.bank_account = bank_account
            affiliate.save()
        
        # Serialize response
        response_serializer = AffiliateSerializer(affiliate)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class GenerateReferralLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Check if user is an approved affiliate
        if not hasattr(request.user, 'affiliate') or request.user.affiliate.status != 'approved':
            return Response({
                'error': 'You must be an approved affiliate to generate referral links'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateReferralLinkSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        affiliate = request.user.affiliate
        campaign = serializer.validated_data['campaign']
        
        # Generate unique URL
        base_url = "http://localhost:3000"  # Frontend URL
        referral_url = f"{base_url}/ref/{affiliate.referral_code}?campaign={campaign}"
        
        # Create referral link
        referral_link, created = ReferralLink.objects.get_or_create(
            affiliate=affiliate,
            campaign=campaign,
            defaults={'url': referral_url}
        )
        
        if not created:
            return Response({
                'error': f'Referral link for campaign "{campaign}" already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize response
        response_serializer = ReferralLinkSerializer(referral_link)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class GetCommissionsView(ListAPIView):
    serializer_class = CommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if hasattr(self.request.user, 'affiliate'):
            return Commission.objects.filter(
                affiliate=self.request.user.affiliate
            ).select_related('referral', 'order')
        return Commission.objects.none()

class RequestPayoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Check if user is an approved affiliate
        if not hasattr(request.user, 'affiliate') or request.user.affiliate.status != 'approved':
            return Response({
                'error': 'You must be an approved affiliate to request payouts'
            }, status=status.HTTP_403_FORBIDDEN)
        
        affiliate = request.user.affiliate
        
        serializer = CreatePayoutSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check minimum payout amount
        if serializer.validated_data['amount'] < 10.00:
            return Response({
                'error': 'Minimum payout amount is $10.00'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create payout request
        payout = Payout.objects.create(
            affiliate=affiliate,
            amount=serializer.validated_data['amount'],
            payment_method=serializer.validated_data['payment_method']
        )
        
        # Update affiliate earnings (this would typically happen after approval)
        affiliate.pending_earnings -= payout.amount
        affiliate.save()
        
        # Serialize response
        response_serializer = PayoutSerializer(payout)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class AffiliateAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is an affiliate
        if not hasattr(request.user, 'affiliate'):
            return Response({
                'error': 'You are not registered as an affiliate'
            }, status=status.HTTP_403_FORBIDDEN)
        
        affiliate = request.user.affiliate
        
        # Get period from query params
        period = request.query_params.get('period', '30d')
        
        if period == '7d':
            days = 7
        elif period == '30d':
            days = 30
        elif period == '90d':
            days = 90
        else:
            days = 30
        
        start_date = timezone.now() - timedelta(days=days)
        
        # Calculate analytics
        commissions_data = self._get_commissions_data(affiliate, start_date)
        referrals_data = self._get_referrals_data(affiliate, start_date)
        clicks_data = self._get_clicks_data(affiliate, start_date)
        
        # Calculate growth (compared to previous period)
        previous_start_date = start_date - timedelta(days=days)
        previous_commissions = Commission.objects.filter(
            affiliate=affiliate,
            created_at__range=[previous_start_date, start_date],
            status__in=['approved', 'paid']
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        current_commissions = commissions_data['total_commissions']
        
        if previous_commissions > 0:
            commission_growth = ((current_commissions - previous_commissions) / previous_commissions) * 100
        else:
            commission_growth = 100 if current_commissions > 0 else 0
        
        # Calculate conversion rate
        total_clicks = clicks_data['total_clicks']
        conversions = referrals_data['converted_count']
        
        if total_clicks > 0:
            conversion_rate = (conversions / total_clicks) * 100
        else:
            conversion_rate = 0
        
        # Calculate click-through rate (simplified)
        total_links = affiliate.referral_links.count()
        if total_links > 0:
            click_through_rate = (total_clicks / total_links) * 100
        else:
            click_through_rate = 0
        
        # Calculate average commission
        commission_count = Commission.objects.filter(
            affiliate=affiliate,
            created_at__gte=start_date
        ).count()
        
        if commission_count > 0:
            average_commission = current_commissions / commission_count
        else:
            average_commission = 0
        
        # Get commissions by period
        commissions_by_period = self._get_commissions_by_period(affiliate, days)
        
        analytics_data = {
            'total_commissions': float(current_commissions),
            'commission_growth': round(float(commission_growth), 2),
            'available_balance': float(affiliate.pending_earnings),
            'pending_commissions': float(affiliate.pending_earnings),
            'total_referrals': referrals_data['total_referrals'],
            'conversion_rate': round(float(conversion_rate), 2),
            'click_through_rate': round(float(click_through_rate), 2),
            'total_clicks': clicks_data['total_clicks'],
            'average_commission': round(float(average_commission), 2),
            'commissions_by_period': commissions_by_period
        }
        
        serializer = AffiliateAnalyticsSerializer(analytics_data)
        return Response(serializer.data)
    
    def _get_commissions_data(self, affiliate, start_date):
        commissions = Commission.objects.filter(
            affiliate=affiliate,
            created_at__gte=start_date,
            status__in=['approved', 'paid']
        ).aggregate(
            total_commissions=Sum('amount')
        )
        
        return {
            'total_commissions': commissions['total_commissions'] or 0
        }
    
    def _get_referrals_data(self, affiliate, start_date):
        referrals = Referral.objects.filter(
            affiliate=affiliate,
            clicked_at__gte=start_date
        )
        
        return {
            'total_referrals': referrals.count(),
            'converted_count': referrals.filter(status='converted').count()
        }
    
    def _get_clicks_data(self, affiliate, start_date):
        clicks = ReferralLink.objects.filter(
            affiliate=affiliate,
            created_at__gte=start_date
        ).aggregate(total_clicks=Sum('clicks'))
        
        return {
            'total_clicks': clicks['total_clicks'] or 0
        }
    
    def _get_commissions_by_period(self, affiliate, days):
        commissions_by_period = []
        
        for i in range(days, 0, -1):
            date = timezone.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            daily_commissions = Commission.objects.filter(
                affiliate=affiliate,
                created_at__date=date.date(),
                status__in=['approved', 'paid']
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            commissions_by_period.append({
                'date': date_str,
                'commissions': float(daily_commissions)
            })
        
        return commissions_by_period

class AffiliateDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, 'affiliate'):
            return Response({
                'error': 'You are not registered as an affiliate'
            }, status=status.HTTP_403_FORBIDDEN)
        
        affiliate = request.user.affiliate
        
        # Get recent commissions
        recent_commissions = Commission.objects.filter(
            affiliate=affiliate
        ).select_related('referral', 'order')[:5]
        
        # Get referral links
        referral_links = ReferralLink.objects.filter(affiliate=affiliate)
        
        # Get recent payouts
        recent_payouts = Payout.objects.filter(affiliate=affiliate)[:5]
        
        commissions_serializer = CommissionSerializer(recent_commissions, many=True)
        links_serializer = ReferralLinkSerializer(referral_links, many=True)
        payouts_serializer = PayoutSerializer(recent_payouts, many=True)
        
        return Response({
            'affiliate': AffiliateSerializer(affiliate).data,
            'recent_commissions': commissions_serializer.data,
            'referral_links': links_serializer.data,
            'recent_payouts': payouts_serializer.data
        })