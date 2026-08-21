from .models import Category, Product


def recently_viewed_products(request):
    viewed_ids = request.session.get('recently_viewed', [])
    products = Product.objects.filter(id__in=viewed_ids).select_related('category')

    products_dict = {p.id: p for p in products}
    ordered_products = [products_dict[p_id] for p_id in viewed_ids if p_id in products_dict]
    
    return {'recently_viewed': ordered_products}


def global_categories(request):
    """Make root categories available on every page for the radial nav menu."""
    from django.core.cache import cache
    cats = cache.get('nav_root_categories')
    if cats is None:
        cats = list(Category.objects.filter(parent=None).prefetch_related('children'))
        cache.set('nav_root_categories', cats, 60 * 15)
    return {'nav_categories': cats}