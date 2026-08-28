from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from shop.models import Product

from .forms import OrderCheckoutForm, ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

SESSION_ADDRESS_KEY = 'checkout_address'


def _get_promocode_context(request, subtotal):
    from promocode.models import Promocode

    promocode = None
    promocode_id = request.session.get('promocode_id')
    if promocode_id:
        promocode = Promocode.objects.filter(id=promocode_id).first()
        if not promocode or not promocode.is_valid():
            promocode = None

    discount_amount = Decimal('0.00')
    if promocode:
        discount_amount = (subtotal * Decimal(promocode.value) / Decimal('100')).quantize(Decimal('0.01'))

    return {
        'promocode': promocode,
        'original_price': subtotal,
        'discount_amount': discount_amount,
        'final_price': subtotal - discount_amount,
    }


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'Скарбниця порожня. Додайте реліквії перед оформленням')
        return redirect('shop:product_list')

    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            request.session[SESSION_ADDRESS_KEY] = form.cleaned_data
            return redirect('orders:checkout_confirm')
        messages.error(request, 'Перевірте правильність заповнення форми.')

    price_context = _get_promocode_context(request, cart.get_total_price())

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
        **price_context,
    })


@login_required
def checkout_confirm(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'Скарбниця порожня. Додайте реліквії перед оформленням')
        return redirect('shop:product_list')

    address_data = request.session.get(SESSION_ADDRESS_KEY)
    if not address_data:
        messages.warning(request, 'Спочатку вкажіть адресу доставки')
        return redirect('orders:checkout')

    price_context = _get_promocode_context(request, cart.get_total_price())
    form = OrderCheckoutForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                order = _create_order(
                    user=request.user,
                    cart=cart,
                    address_data=address_data,
                    payment_method=form.cleaned_data['payment_method'],
                    notes=form.cleaned_data['notes'],
                    promocode=price_context['promocode'],
                    discount_amount=price_context['discount_amount'],
                )
            except ValueError as exc:
                messages.error(request, f'Не вдалося створити замовлення: {exc}')
                return redirect('cart:cart_detail')

            cart.clear()
            request.session.pop(SESSION_ADDRESS_KEY, None)
            for key in ('promocode_id', 'promocode_code', 'promocode_value'):
                request.session.pop(key, None)

            messages.success(request, f'Замовлення #{order.order_number} успішно оформлено!')

            from .emails import send_order_confirmation_email, notify_admins_about_order
            send_order_confirmation_email(order)
            notify_admins_about_order(order)

            if order.requires_online_payment:
                return redirect('payments:initiate_payment', order_number=order.order_number)
            return redirect('orders:order_success', order_id=order.id)
        messages.error(request, 'Перевірте правильність заповнення форми.')

    return render(request, 'orders/checkout_confirm.html', {
        'cart': cart,
        'address': address_data,
        'form': form,
        **price_context,
    })


@transaction.atomic
def _create_order(user, cart, address_data, payment_method, notes, promocode, discount_amount):

    items = list(cart)
    if not items:
        raise ValueError('скарбниця порожня')

    subtotal = cart.get_total_price()

    order = Order.objects.create(
        user=user,
        total_price=subtotal - discount_amount,
        payment_method=payment_method,
        notes=notes,
        coupon=promocode,
        discount=promocode.value if promocode else 0,
    )

    ShippingAddress.objects.create(order=order, **address_data)

    for item in items:
        product = Product.objects.select_for_update().get(pk=item['product'].pk)

        if product.stock < item['quantity']:
            raise ValueError(f'недостатньо товару «{product.name}» на складі')

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            price=product.price,
            quantity=item['quantity'],
        )

        Product.objects.filter(pk=product.pk).update(stock=F('stock') - item['quantity'])

    if promocode:
        promocode.times_used = F('times_used') + 1
        promocode.save(update_fields=['times_used'])

    return order


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).select_related('coupon').prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('coupon', 'shipping_address').prefetch_related('items__product', 'status_history'),
        id=order_id,
        user=request.user,
    )
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_be_cancelled():
        messages.error(
            request,
            'Скасувати замовлення неможливо — '
            'або пройшло більше 24 годин, або воно вже відправлено'
        )
        return redirect('orders:order_detail', order_id=order.id)

    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Замовлення #{order.id} скасовано.')
        return redirect('orders:order_list')

    return redirect('orders:order_detail', order_id=order.id)


@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items', 'shipping_address'),
        id=order_id,
        user=request.user,
    )
    from .pdf import generate_order_pdf
    return generate_order_pdf(order)
