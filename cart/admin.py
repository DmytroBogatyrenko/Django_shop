from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_code', 'user', 'paid_status', 'created_at', 'modified_at']
    list_filter = ['paid_status', 'created_at']
    search_fields = ['cart_code', 'user__username', 'user__email']
    inlines = [CartItemInline]
