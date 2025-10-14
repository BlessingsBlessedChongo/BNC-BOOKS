from django.contrib import admin
from .models import Affiliate, ReferralLink, Referral, Commission, Payout

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'commission_rate', 'total_earnings', 'pending_earnings', 'joined_at')
    list_filter = ('status', 'is_active', 'joined_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'referral_code')
    readonly_fields = ('joined_at', 'approved_at')
    list_editable = ('status', 'commission_rate')
    
    fieldsets = (
        ('Affiliate Information', {
            'fields': ('user', 'status', 'commission_rate', 'referral_code')
        }),
        ('Payment Information', {
            'fields': ('paypal_email', 'bank_account', 'preferred_payment_method')
        }),
        ('Earnings', {
            'fields': ('total_earnings', 'paid_earnings', 'pending_earnings')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('joined_at', 'approved_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReferralLink)
class ReferralLinkAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'campaign', 'clicks', 'conversions', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('affiliate__user__email', 'campaign', 'url')
    readonly_fields = ('created_at',)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'user', 'status', 'clicked_at', 'converted_at')
    list_filter = ('status', 'clicked_at')
    search_fields = ('affiliate__user__email', 'user__email')
    readonly_fields = ('clicked_at', 'registered_at', 'converted_at')

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'amount', 'commission_rate', 'type', 'status', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('affiliate__user__email', 'description')
    readonly_fields = ('created_at', 'approved_at', 'paid_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Commission Information', {
            'fields': ('affiliate', 'referral', 'order', 'amount', 'commission_rate')
        }),
        ('Details', {
            'fields': ('type', 'status', 'description', 'calculated_on')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'approved_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'amount', 'payment_method', 'status', 'requested_at', 'paid_at')
    list_filter = ('status', 'payment_method', 'requested_at')
    search_fields = ('affiliate__user__email', 'payment_reference')
    readonly_fields = ('requested_at', 'processed_at', 'paid_at')
    list_editable = ('status',)