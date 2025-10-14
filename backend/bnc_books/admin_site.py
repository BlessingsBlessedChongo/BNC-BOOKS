from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class BNCBooksAdminSite(AdminSite):
    site_header = _("BNC Books Administration")
    site_title = _("BNC Books Admin Portal")
    index_title = _("Welcome to BNC Books Administration")

# Create instance
admin_site = BNCBooksAdminSite(name='admin')

# Register all models
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin, GroupAdmin

# Unregister default models
admin.site.unregister(Group)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register with custom site
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)

# Now import and register all your app models
from accounts.models import User, UserProfile
from accounts.admin import CustomUserAdmin, UserProfileAdmin
from books.models import Book, Category, Genre
from books.admin import BookAdmin, CategoryAdmin, GenreAdmin
from orders.models import Order, OrderItem, Cart, CartItem, ShippingMethod
from orders.admin import OrderAdmin, OrderItemAdmin, CartAdmin, CartItemAdmin, ShippingMethodAdmin
from reviews.models import Review, ReviewVote, ReviewReport
from reviews.admin import ReviewAdmin, ReviewVoteAdmin, ReviewReportAdmin
from affiliates.models import Affiliate, ReferralLink, Referral, Commission, Payout
from affiliates.admin import AffiliateAdmin, ReferralLinkAdmin, ReferralAdmin, CommissionAdmin, PayoutAdmin
from analytics.models import SellerAnalytics, DailySales, BookPerformance, InventoryAlert, SalesReport
from analytics.admin import SellerAnalyticsAdmin, DailySalesAdmin, BookPerformanceAdmin, InventoryAlertAdmin, SalesReportAdmin

# Register all models
admin_site.register(User, CustomUserAdmin)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(Book, BookAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Genre, GenreAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(OrderItem, OrderItemAdmin)
admin_site.register(Cart, CartAdmin)
admin_site.register(CartItem, CartItemAdmin)
admin_site.register(ShippingMethod, ShippingMethodAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(ReviewVote, ReviewVoteAdmin)
admin_site.register(ReviewReport, ReviewReportAdmin)
admin_site.register(Affiliate, AffiliateAdmin)
admin_site.register(ReferralLink, ReferralLinkAdmin)
admin_site.register(Referral, ReferralAdmin)
admin_site.register(Commission, CommissionAdmin)
admin_site.register(Payout, PayoutAdmin)
admin_site.register(SellerAnalytics, SellerAnalyticsAdmin)
admin_site.register(DailySales, DailySalesAdmin)
admin_site.register(BookPerformance, BookPerformanceAdmin)
admin_site.register(InventoryAlert, InventoryAlertAdmin)
admin_site.register(SalesReport, SalesReportAdmin)