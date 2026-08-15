from django.contrib import admin
from .models import Promocode
# Register your models here.
@admin.register(Promocode)
class Promocode_admin(admin.ModelAdmin):
    list_display = ["code", "value", "date_start", "valid_date", "max_uses", "times_used"]
    list_display_links = ['code']

    readonly_fields = ['times_used', 'date_start']
    