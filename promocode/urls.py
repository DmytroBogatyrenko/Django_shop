from django.urls import path
from . import views

app_name = 'promocode'

urlpatterns = [
    path('apply/', views.apply_promocode, name='apply'),
    path('remove/', views.remove_promocode, name='remove'),
]