from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity', 'get_total_price']

    def get_total_price(self, obj):
        return f'{obj.get_total_price()} грн'
    get_total_price.short_description = 'Сума'


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_display_links = ['id', 'user']
    list_per_page = 20
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'user__username', 'shipping_address__email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    inlines = [ShippingAddressInline, OrderItemInline]