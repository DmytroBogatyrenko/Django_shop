from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from orders.models import Order
from shop.models import Category, Product

from .models import Transaction

User = get_user_model()


class PaymentsFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='buyer', password='testpass123', email='buyer@citadel.ua',
        )
        category = Category.objects.create(name='Артефакти')
        self.product = Product.objects.create(
            name='Амулет Долі', category=category,
            price='100.00', slug='amulet-doli', stock=5,
        )
        self.client.login(username='buyer', password='testpass123')

    def _create_card_order(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})

        address = {
            'first_name': 'Тест', 'last_name': 'Тестенко',
            'email': 'test@test.ua', 'phone': '+380990000000',
            'city': 'Київ', 'address': 'вул. Тестова, 1',
            'postal_code': '01000',
        }
        self.client.post(reverse('orders:checkout'), address)
        self.client.post(reverse('orders:checkout_confirm'), {
            'payment_method': 'card', 'notes': '',
        })
        return Order.objects.get(user=self.user)

    def test_card_order_requires_online_payment(self):
        order = self._create_card_order()
        self.assertTrue(order.requires_online_payment)
        self.assertEqual(order.status, 'pending')

    def test_initiate_payment_creates_transaction(self):
        order = self._create_card_order()
        response = self.client.get(
            reverse('payments:initiate_payment', args=[order.order_number])
        )
        self.assertEqual(response.status_code, 200)

        transaction = Transaction.objects.get(order=order)
        self.assertEqual(transaction.status, Transaction.STATUS_SPENDING)
        self.assertEqual(transaction.amount, order.total_price)

    def test_successful_callback_marks_order_paid(self):
        order = self._create_card_order()
        self.client.get(reverse('payments:initiate_payment', args=[order.order_number]))
        transaction = Transaction.objects.get(order=order)

        response = self.client.get(reverse('payments:payment_callback'), {
            'tx_ref': transaction.reference,
            'status': 'successful',
            'transaction_id': 'MOCK-1',
        })
        self.assertEqual(response.status_code, 302)

        order.refresh_from_db()
        transaction.refresh_from_db()
        self.assertTrue(order.is_paid)
        self.assertEqual(order.status, 'paid')
        self.assertEqual(transaction.status, Transaction.STATUS_COMPLETED)

    def test_failed_callback_marks_transaction_failed(self):
        order = self._create_card_order()
        self.client.get(reverse('payments:initiate_payment', args=[order.order_number]))
        transaction = Transaction.objects.get(order=order)

        response = self.client.get(reverse('payments:payment_callback'), {
            'tx_ref': transaction.reference,
            'status': 'failed',
            'transaction_id': 'MOCK-2',
        })
        self.assertEqual(response.status_code, 302)

        order.refresh_from_db()
        transaction.refresh_from_db()
        self.assertFalse(order.is_paid)
        self.assertEqual(transaction.status, Transaction.STATUS_FAILED)

    def test_cash_order_skips_payments_app(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        address = {
            'first_name': 'Готів', 'last_name': 'Кою',
            'email': 'cash@test.ua', 'phone': '+380990000001',
            'city': 'Львів', 'address': 'вул. Готівкова, 1',
            'postal_code': '02000',
        }
        self.client.post(reverse('orders:checkout'), address)
        response = self.client.post(reverse('orders:checkout_confirm'), {
            'payment_method': 'cash', 'notes': '',
        })
        order = Order.objects.get(user=self.user)
        self.assertFalse(order.requires_online_payment)
        self.assertRedirects(response, reverse('orders:order_success', args=[order.id]))
        self.assertFalse(Transaction.objects.filter(order=order).exists())
