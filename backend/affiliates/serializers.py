from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import Affiliate, ReferralLink, Referral, Commission, Payout
from accounts.serializers import UserSerializer

class BankAccountSerializer(serializers.Serializer):
    account_holder = serializers.CharField(max_length=100, required=True)
    account_number = serializers.CharField(max_length=50, required=True)
    routing_number = serializers.CharField(max_length=20, required=True)
    bank_name = serializers.CharField(max_length=100, required=True)

class AffiliateRegistrationSerializer(serializers.ModelSerializer):
    bank_account = BankAccountSerializer(required=False)
    
    class Meta:
        model = Affiliate
        fields = (
            'paypal_email', 'bank_account', 'preferred_payment_method'
        )
    
    def validate_paypal_email(self, value):
        if value:
            validator = EmailValidator()
            validator(value)
        return value
    
    def validate(self, data):
        preferred_payment_method = data.get('preferred_payment_method')
        paypal_email = data.get('paypal_email')
        bank_account = data.get('bank_account')
        
        if preferred_payment_method == 'paypal' and not paypal_email:
            raise serializers.ValidationError({
                'paypal_email': 'PayPal email is required for PayPal payments.'
            })
        
        if preferred_payment_method == 'bank_transfer' and not bank_account:
            raise serializers.ValidationError({
                'bank_account': 'Bank account details are required for bank transfers.'
            })
        
        return data

class AffiliateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Affiliate
        fields = (
            'id', 'user', 'status', 'commission_rate', 'paypal_email',
            'bank_account', 'preferred_payment_method', 'total_earnings',
            'paid_earnings', 'pending_earnings', 'referral_code', 'is_active',
            'joined_at', 'approved_at'
        )
        read_only_fields = (
            'status', 'commission_rate', 'total_earnings', 'paid_earnings',
            'pending_earnings', 'referral_code', 'is_active', 'joined_at', 'approved_at'
        )

class ReferralLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralLink
        fields = (
            'id', 'campaign', 'url', 'clicks', 'conversions', 
            'is_active', 'created_at'
        )
        read_only_fields = ('url', 'clicks', 'conversions', 'created_at')

class CreateReferralLinkSerializer(serializers.Serializer):
    campaign = serializers.CharField(max_length=100, required=True)
    
    def validate_campaign(self, value):
        # Remove any special characters and spaces
        import re
        cleaned_campaign = re.sub(r'[^a-zA-Z0-9_]', '_', value)
        return cleaned_campaign

class ReferralSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    affiliate_email = serializers.EmailField(source='affiliate.user.email', read_only=True)
    
    class Meta:
        model = Referral
        fields = (
            'id', 'affiliate', 'affiliate_email', 'referral_link', 
            'user', 'user_email', 'status', 'clicked_at', 
            'registered_at', 'converted_at'
        )
        read_only_fields = ('affiliate', 'user', 'status', 'clicked_at', 'registered_at', 'converted_at')

class CommissionSerializer(serializers.ModelSerializer):
    referral = ReferralSerializer(read_only=True)
    order_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Commission
        fields = (
            'id', 'amount', 'commission_rate', 'type', 'status', 
            'description', 'calculated_on', 'referral', 'order_info',
            'created_at', 'approved_at', 'paid_at'
        )
        read_only_fields = ('created_at', 'approved_at', 'paid_at')
    
    def get_order_info(self, obj):
        if obj.order:
            return {
                'id': obj.order.id,
                'order_number': obj.order.order_number,
                'total_amount': obj.order.total_amount
            }
        return None

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = (
            'id', 'amount', 'payment_method', 'status', 
            'payment_reference', 'notes', 'requested_at',
            'processed_at', 'paid_at'
        )
        read_only_fields = ('status', 'payment_reference', 'requested_at', 'processed_at', 'paid_at')

class CreatePayoutSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=10.00,  # Minimum payout amount
        required=True
    )
    payment_method = serializers.ChoiceField(
        choices=Affiliate.PAYMENT_METHOD_CHOICES,
        required=True
    )
    
    def validate_amount(self, value):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            affiliate = request.user.affiliate
            if value > affiliate.pending_earnings:
                raise serializers.ValidationError(
                    f"Requested amount (${value}) exceeds available balance (${affiliate.pending_earnings})"
                )
        return value

class AffiliateAnalyticsSerializer(serializers.Serializer):
    total_commissions = serializers.DecimalField(max_digits=12, decimal_places=2)
    commission_growth = serializers.DecimalField(max_digits=5, decimal_places=2)
    available_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_commissions = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_referrals = serializers.IntegerField()
    conversion_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    click_through_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_clicks = serializers.IntegerField()
    average_commission = serializers.DecimalField(max_digits=10, decimal_places=2)
    commissions_by_period = serializers.ListField()