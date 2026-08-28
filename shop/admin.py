from django.contrib import admin

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    list_filter = ["parent"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "category", "is_featured", "created_at"]
    list_filter = ["category", "is_featured"]
    search_fields = ["name"]
    list_editable = ["is_featured", "stock"]
    prepopulated_fields = {"slug": ("name",)}

    inlines = [ProductImageInline]
    list_per_page = 20
