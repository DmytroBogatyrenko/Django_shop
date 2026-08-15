from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from promocode.models import Promocode
from .forms import ShippingAddressForm
from .models import Order, OrderItem


def get_promocode_from_session(request):

    promocode_id = request.session.get('promocode_id')
    if promocode_id:
        try:
            return Promocode.objects.get(id=promocode_id)
        except Promocode.DoesNotExist:
            del request.session['promocode_id']
    return None


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect('shop:product_list')

    promocode = get_promocode_from_session(request)

    original_price = cart.get_total_price()
    discount_percent = promocode.value if promocode else 0
    discount_amount = original_price * Decimal(discount_percent) / Decimal('100')
    final_price = original_price - discount_amount

    form = ShippingAddressForm()

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=final_price,
                    coupon=promocode,
                    discount=discount_percent,
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

                if promocode:
                    promocode.times_used += 1
                    promocode.save()
                    for key in ['promocode_id', 'promocode_code', 'promocode_value']:
                        request.session.pop(key, None)

                cart.clear()

            return redirect('orders:thank_you', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
        'promocode': promocode,
        'original_price': original_price,
        'discount_amount': discount_amount,
        'final_price': final_price,
    })


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