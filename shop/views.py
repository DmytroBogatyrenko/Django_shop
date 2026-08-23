from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request, category_id=None):
    categories = cache.get('root_categories')
    if categories is None:
        categories = list(
            Category.objects.filter(parent=None).prefetch_related('children')
        )
        cache.set('root_categories', categories, 60 * 15)

    category = None
    products = Product.objects.all().select_related('category').prefetch_related('images')

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query))

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')

    featured_products = None
    if not category_id and not query:
        featured_products = (
            Product.objects
            .filter(is_featured=True)
            .select_related('category')
            .prefetch_related('images')[:4]
        )

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'shop/product_list.html', {
        'selected_category': category,
        'categories': categories,
        'products': products_page,
        'featured_products': featured_products,
        'query': query,
        'sort': sort,
    })


def product_detail(request, id, slug):
    cache_key = f'product_{id}'
    product = cache.get(cache_key)

    if product is None:
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('images'),
            id=id, slug=slug,
        )
        cache.set(cache_key, product, 60 * 15)

    recently_viewed = request.session.get('recently_viewed', [])
    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)
    request.session['recently_viewed'] = recently_viewed[:10]
    request.session.modified = True

    from django.db.models import Avg
    reviews = []
    avg_rating = None
    try:
        from reviews.models import Review
        reviews = Review.objects.filter(
            product=product, is_approved=True
        ).select_related('user').order_by('-created_at')
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    except Exception:
        pass

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


def search_autocomplete(request):
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'results': []})

    products = (
        Product.objects
        .filter(name__icontains=query)
        .select_related('category')
        [:8]
    )

    results = [
        {
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'category': p.category.name,
            'url': p.get_absolute_url(),
        }
        for p in products
    ]

    return JsonResponse({'results': results})