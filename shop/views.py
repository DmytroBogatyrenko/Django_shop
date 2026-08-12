from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category


def product_list(request, category_id=None):
    category = None
    categories = Category.objects.filter(parent=None).prefetch_related('children')
    
    products = Product.objects.all().select_related('category')

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

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'shop/product_list.html', {
        'selected_category': category,
        'categories': categories,
        'products': products_page,
        'query': query,
        'sort': sort,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)

    recently_viewed = request.session.get('recently_viewed', [])
    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)

    request.session['recently_viewed'] = recently_viewed[:10]
    request.session.modified = True

    return render(request, 'shop/product_detail.html', {'product': product})