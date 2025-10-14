from datetime import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from decimal import Decimal 

class Affiliate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('suspended', 'Suspended'),
        ('rejected', 'Rejected'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='affiliate'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=10.00,  # 10% default commission
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))] 
    )
    paypal_email = models.EmailField(blank=True, null=True)
    bank_account = models.JSONField(blank=True, null=True)  # Store bank details as JSON
    preferred_payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='paypal'
    )
    total_earnings = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    paid_earnings = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    pending_earnings = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    referral_code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"Affiliate: {self.user.email}"
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self._generate_referral_code()
        super().save(*args, **kwargs)
    
    def _generate_referral_code(self):
        import random
        import string
        
        while True:
            code = 'AFF' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            if not Affiliate.objects.filter(referral_code=code).exists():
                return code

class ReferralLink(models.Model):
    affiliate = models.ForeignKey(
        Affiliate, 
        on_delete=models.CASCADE, 
        related_name='referral_links'
    )
    campaign = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['affiliate', 'campaign']
    
    def __str__(self):
        return f"{self.campaign} - {self.affiliate.user.email}"

class Referral(models.Model):
    STATUS_CHOICES = [
        ('clicked', 'Clicked'),
        ('registered', 'Registered'),
        ('converted', 'Converted'),  # Made a purchase
        ('expired', 'Expired'),
    ]
    
    affiliate = models.ForeignKey(
        Affiliate, 
        on_delete=models.CASCADE, 
        related_name='referrals'
    )
    referral_link = models.ForeignKey(
        ReferralLink, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='referrals'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='referrals_received'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='clicked'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    registered_at = models.DateTimeField(null=True, blank=True)
    converted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-clicked_at']
        unique_together = ['affiliate', 'user']
    
    def __str__(self):
        return f"Referral: {self.user.email} by {self.affiliate.user.email}"

class Commission(models.Model):
    TYPE_CHOICES = [
        ('sale', 'Sale'),
        ('signup', 'Signup Bonus'),
        ('bonus', 'Bonus'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    affiliate = models.ForeignKey(
        Affiliate, 
        on_delete=models.CASCADE, 
        related_name='commissions'
    )
    referral = models.ForeignKey(
        Referral, 
        on_delete=models.CASCADE, 
        related_name='commissions',
        null=True, 
        blank=True
    )
    order = models.ForeignKey(
        'orders.Order', 
        on_delete=models.CASCADE, 
        related_name='commissions',
        null=True, 
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from django.core.validators import MinValueValidator
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))] 
    )
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='sale')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    calculated_on = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Amount the commission was calculated on"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commission: ${self.amount} - {self.affiliate.user.email}"

class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    affiliate = models.ForeignKey(
        Affiliate, 
        on_delete=models.CASCADE, 
        related_name='payouts'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Affiliate.PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_reference = models.CharField(max_length=100, blank=True)
    paypal_transaction_id = models.CharField(max_length=100, blank=True)
    bank_transfer_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Payout: ${self.amount} - {self.affiliate.user.email}"
    
    def save(self, *args, **kwargs):
        if self.status == 'paid' and not self.paid_at:
            self.paid_at = timezone.now()
        super().save(*args, **kwargs)