from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from shop.models import Category, Product
from .models import Order, OrderItem, ShippingAddress


# Create your tests here.

User = get_user_model()


class CheckoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        category = Category.objects.create(name='Зілля')
        self.product = Product.objects.create(
            name='Зілля Сили', category=category,
            price='350.00', slug='zillia-syly', stock=10,
        )

    def test_checkout_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_checkout_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1})
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)

    def test_checkout_redirects_empty_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 302)

    def test_checkout_creates_order(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 2})

        address_data = {
            'first_name': 'Артур', 'last_name': 'Пендрагон',
            'email': 'arthur@citadel.ua', 'phone': '+380991234567',
            'city': 'Камелот', 'address': 'вул. Лицарів, 1',
            'postal_code': '01000',
        }
        response = self.client.post(reverse('orders:checkout'), address_data)
        self.assertRedirects(response, reverse('orders:checkout_confirm'))

        response = self.client.post(reverse('orders:checkout_confirm'), {
            'payment_method': 'cash', 'notes': '',
        })
        self.assertEqual(response.status_code, 302)

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product_name, 'Зілля Сили')


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass')
        self.order = Order.objects.create(user=self.user, total_price='500.00')

    def test_order_str_contains_id(self):
        self.assertIn(str(self.order.id), str(self.order))

    def test_order_default_status_is_pending(self):
        self.assertEqual(self.order.status, 'pending')
