from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'is_verified_purchase', 'is_approved', 'created_at', 'helpful_votes']
    list_filter = ['rating', 'is_verified_purchase', 'is_approved', 'created_at']
    search_fields = ['user__username', 'product__name', 'text']
    actions = ['approve_reviews', 'disapprove_reviews']

    @admin.action(description='Схвалити вибрані відгуки')
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Відхилити вибрані відгуки')
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)