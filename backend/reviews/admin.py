from django.contrib import admin
from .models import Review, ReviewVote, ReviewReport

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'title', 'verified_purchase', 'is_approved', 'created_at')
    list_filter = ('rating', 'verified_purchase', 'is_approved', 'created_at')
    search_fields = ('user__email', 'book__title', 'title')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_approved',)
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'book', 'rating', 'title', 'comment')
        }),
        ('Additional Details', {
            'fields': ('pros', 'cons', 'would_recommend', 'verified_purchase')
        }),
        ('Statistics', {
            'fields': ('helpful_count', 'not_helpful_count')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__email', 'review__title')
    readonly_fields = ('created_at',)

@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'reason', 'is_resolved', 'created_at')
    list_filter = ('reason', 'is_resolved', 'created_at')
    search_fields = ('user__email', 'review__title')
    readonly_fields = ('created_at',)
    list_editable = ('is_resolved',)