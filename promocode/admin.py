from django.contrib import admin
from .models import Promocode
# Register your models here.
@admin.register(Promocode)
class Promocode_admin(admin.ModelAdmin):
    list_display = ["code", "value", "date_start", "valid_date"]
    list_display_links = ['code']
    