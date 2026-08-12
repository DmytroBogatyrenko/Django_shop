from .models import Product

def recently_viewed_products(request):
    viewed_ids = request.session.get('recently_viewed', [])
    products = Product.objects.filter(id__in=viewed_ids).select_related('category')

    products_dict = {p.id: p for p in products}
    ordered_products = [products_dict[p_id] for p_id in viewed_ids if p_id in products_dict]
    
    return {'recently_viewed': ordered_products}