from django.contrib import admin

# Register your models here.
from .models import Product, Category, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category"]
    