from django.contrib import admin
from django.urls import path


class CustomAdminSite(admin.AdminSite):
    site_header = 'Цитадель — Адміністрування'
    site_title  = 'Citadel Admin'
    index_title = 'Панель управління'

    def get_urls(self):
        from shop_project.admin_views import dashboard, export_orders_csv
        urls = super().get_urls()
        custom = [
            path('analytics/', self.admin_view(dashboard), name='analytics_dashboard'),
            path('analytics/export/', self.admin_view(export_orders_csv), name='analytics_export'),
        ]
        return custom + urls
