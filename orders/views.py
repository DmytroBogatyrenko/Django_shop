from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'Скарбниця порожня. Додайте реліквії перед оформленням.')
        return redirect('shop:product_list')

    form = ShippingAddressForm()

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.get_total_price(),
                )
                shipping = form.save(commit=False)
                shipping.order = order
                shipping.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        price=item['price'],
                        quantity=item['quantity'],
                    )
                cart.clear()

            messages.success(request, f'Замовлення #{order.id} успішно оформлено!')
            return redirect('orders:thank_you', order_id=order.id)
        else:
            messages.error(request, 'Перевірте правильність заповнення форми.')

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/thank_you.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user,
    )
    return render(request, 'orders/order_detail.html', {'order': order})
