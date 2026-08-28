from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from orders.models import Order, OrderItem
from shop.models import Category, Product
from .models import Review

User = get_user_model()


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='password123')
        self.non_buyer = User.objects.create_user(username='guest_user', password='password123')
        self.category = Category.objects.create(name='Тест Категорія', slug='test-cat')
        self.product = Product.objects.create(
            name='Тестовий Товар',
            slug='test-prod',
            price=Decimal('100.00'),
            category=self.category,
            stock=10,
        )

        # Створюємо замовлення для користувача buyer
        self.order = Order.objects.create(
            user=self.user,
            total_price=Decimal('100.00'),
            payment_method='cod',
            status='paid',
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            price=self.product.price,
            quantity=1,
        )

    def test_review_creation_verified_purchase(self):
        """Перевірка автоматичного прапорця is_verified_purchase при збереженні."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            text='Чудовий товар!',
        )
        self.assertTrue(review.is_verified_purchase)

        non_verified_review = Review.objects.create(
            user=self.non_buyer,
            product=self.product,
            rating=3,
            text='Звичайний товар',
        )
        self.assertFalse(non_verified_review.is_verified_purchase)

    def test_add_review_view_requires_purchase(self):
        """Перевірка створення відгуку через view: тільки для покупців."""
        self.client.login(username='guest_user', password='password123')
        response = self.client.post(
            reverse('reviews:add_review', kwargs={'product_id': self.product.id}),
            {'rating': 4, 'text': 'Тест відгуку без покупки'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(user=self.non_buyer, product=self.product).exists())

        # Тепер входимо покупцем
        self.client.login(username='buyer', password='password123')
        response = self.client.post(
            reverse('reviews:add_review', kwargs={'product_id': self.product.id}),
            {'rating': 5, 'text': 'Гарний товар від покупця'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, product=self.product).exists())

    def test_vote_review(self):
        """Перевірка голосування за корисність відгуку."""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            text='Корисний відгук',
        )
        url = reverse('reviews:vote_review', kwargs={'review_id': review.id})
        response = self.client.post(url, {'vote_type': 'helpful'})
        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.helpful_votes, 1)
