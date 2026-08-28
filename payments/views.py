import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from orders.models import Order, OrderStatusHistory

from .models import Transaction


def _calculate_total(order):
    tax_rate = Decimal(settings.PAYMENT_TAX_RATE)
    tax = (order.total_price * tax_rate).quantize(Decimal('0.01'))
    return order.total_price + tax


@login_required
def initiate_payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if order.is_paid:
        messages.info(request, 'Це замовлення вже оплачено')
        return redirect('orders:order_detail', order_id=order.id)

    tx_ref = uuid.uuid4().hex
    total_amount = _calculate_total(order)

    transaction = Transaction.objects.create(
        reference=tx_ref,
        order=order,
        amount=total_amount,
        currency=settings.PAYMENT_CURRENCY,
        user=request.user,
        status=Transaction.STATUS_SPENDING,
    )

    redirect_url = request.build_absolute_uri(reverse('payments:payment_callback'))

    hosted_link = reverse('payments:mock_gateway', args=[tx_ref])

    return render(request, 'payments/initiate.html', {
        'order': order,
        'transaction': transaction,
        'hosted_link': hosted_link,
        'redirect_url': redirect_url,
    })


@login_required
def mock_gateway(request, tx_ref):
    transaction = get_object_or_404(Transaction, reference=tx_ref, user=request.user)

    if transaction.status != Transaction.STATUS_SPENDING:
        messages.info(request, 'Цю транзакцію вже оброблено')
        return redirect('orders:order_detail', order_id=transaction.order.id)

    return render(request, 'payments/mock_gateway.html', {'transaction': transaction})


@login_required
def payment_callback(request):

    tx_ref = request.GET.get('tx_ref')
    gateway_status = request.GET.get('status')
    gateway_transaction_id = request.GET.get('transaction_id', '')

    transaction = get_object_or_404(Transaction, reference=tx_ref, user=request.user)

    if transaction.status == Transaction.STATUS_COMPLETED:
        messages.info(request, 'Оплату вже підтверджено раніше')
        return redirect('orders:order_detail', order_id=transaction.order.id)


    verification = {
        'status': gateway_status,
        'amount': str(transaction.amount),
        'currency': transaction.currency,
    }

    checks_passed = (
        verification['status'] == 'successful'
        and Decimal(verification['amount']) == transaction.amount
        and verification['currency'] == transaction.currency
    )

    if not checks_passed:
        transaction.status = Transaction.STATUS_FAILED
        transaction.gateway_transaction_id = gateway_transaction_id
        transaction.save(update_fields=['status', 'gateway_transaction_id', 'updated_at'])

        messages.error(request, 'Оплату не підтверджено. Спробуйте ще раз.')
        return redirect('orders:order_detail', order_id=transaction.order.id)

    _complete_payment(transaction, gateway_transaction_id)

    messages.success(
        request,
        f'Оплату за замовлення #{transaction.order.order_number} успішно підтверджено!',
    )
    return redirect('orders:order_detail', order_id=transaction.order.id)


@db_transaction.atomic
def _complete_payment(transaction, gateway_transaction_id):
    transaction.status = Transaction.STATUS_COMPLETED
    transaction.gateway_transaction_id = gateway_transaction_id
    transaction.save(update_fields=['status', 'gateway_transaction_id', 'updated_at'])

    order = transaction.order
    order.status = 'paid'
    order.save(update_fields=['status', 'updated_at'])

    OrderStatusHistory.objects.create(
        order=order,
        old_status='pending',
        new_status='paid',
        comment=f'Оплату підтверджено. Транзакція {transaction.reference}',
    )

    from orders.emails import send_payment_received_email
    send_payment_received_email(order)

