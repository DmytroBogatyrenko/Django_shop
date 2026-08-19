from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Category, Product


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_cache(sender, **kwargs):
    cache.delete('root_categories')


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key = f'product_{instance.id}'
    cache.delete(cache_key)
    cache.delete('root_categories')
