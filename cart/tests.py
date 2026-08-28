from django.test import Client, TestCase
from django.urls import reverse

from shop.models import Category, Product


# Create your tests here.

class CartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        category = Category.objects.create(name='Зброя')
        self.product = Product.objects.create(
            name='Меч Долі',
            category=category,
            price='2500.00',
            slug='mech-doli',
            stock=10,
        )
        self.add_url    = reverse('cart:cart_add',    args=[self.product.id])
        self.remove_url = reverse('cart:cart_remove', args=[self.product.id])
        self.detail_url = reverse('cart:cart_detail')

    def test_cart_page_loads(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_cart_uses_correct_template(self):
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, 'cart/detail.html')

    def test_add_product_to_cart(self):
        response = self.client.post(self.add_url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)

    def test_product_appears_in_cart_after_adding(self):
        self.client.post(self.add_url, {'quantity': 1})
        response = self.client.get(self.detail_url)
        self.assertContains(response, 'Меч Долі')

    def test_remove_product_from_cart(self):
        self.client.post(self.add_url, {'quantity': 1})
        response = self.client.post(self.remove_url)
        self.assertEqual(response.status_code, 302)

    def test_cart_shows_empty_message_after_removing(self):
        self.client.post(self.add_url, {'quantity': 1})
        self.client.post(self.remove_url)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'порожня')

    def test_add_requires_post_method(self):
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 405)

    def test_remove_requires_post_method(self):
        response = self.client.get(self.remove_url)
        self.assertEqual(response.status_code, 405)