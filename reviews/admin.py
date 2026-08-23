from django.contrib import admin

# Register your models here.

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'is_verified_purchase',
                    'is_approved', 'created_at']
    list_filter = ['is_approved', 'is_verified_purchase', 'rating']
    search_fields = ['user__username', 'product__name', 'text']
    list_editable = ['is_approved']
    readonly_fields = ['is_verified_purchase', 'created_at']