from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_views import dashboard, export_orders_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('shop.urls', namespace='shop')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('accounts/social/', include('allauth.urls')),
    path('admin/dashboard/', dashboard, name='analytics_dashboard'),
    path('admin/dashboard/export/', export_orders_csv, name='analytics_export'),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)