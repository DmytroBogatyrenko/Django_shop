from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import get_cart

MAX_QUANTITY_PER_PRODUCT = 99


def _parse_quantity(request, default=1):
    try:
        return int(request.POST.get('quantity', default))
    except (TypeError, ValueError):
        return default


def _clamp_quantity(product, quantity):
    if quantity < 1:
        return None, 'Кількість має бути більшою за 0'

    if quantity > MAX_QUANTITY_PER_PRODUCT:
        return None, f'Максимальна кількість одного товару — {MAX_QUANTITY_PER_PRODUCT} шт.'

    if quantity > product.stock:
        return None, f'Доступно тільки {product.stock} од. товару «{product.name}»'

    return quantity, None


@require_POST
def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    if not product.is_in_stock:
        messages.error(request, f'Товару «{product.name}» немає в наявності')
        return redirect('shop:product_detail', id=product.id, slug=product.slug)

    quantity = _parse_quantity(request)
    quantity, error = _clamp_quantity(product, quantity)
    if error:
        messages.error(request, error)
        return redirect('shop:product_detail', id=product.id, slug=product.slug)

    cart.add(product=product, quantity=quantity)
    messages.success(request, f'«{product.name}» додано до скарбниці.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = _parse_quantity(request)

    if quantity <= 0:
        cart.remove(product)
        messages.success(request, f'«{product.name}» видалено зі скарбниці.')
        return redirect('cart:cart_detail')

    quantity, error = _clamp_quantity(product, quantity)
    if error:
        messages.error(request, error)
        return redirect('cart:cart_detail')

    cart.add(product=product, quantity=quantity, update_quantity=True)
    messages.success(request, 'Скарбницю оновлено.')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'«{product.name}» видалено зі скарбниці.')
    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    get_cart(request).clear()
    messages.success(request, 'Скарбницю очищено.')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
