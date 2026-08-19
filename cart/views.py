from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'«{product.name}» додано до скарбниці.')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'«{product.name}» видалено зі скарбниці.')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
