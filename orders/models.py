from django.conf import settings
from django.db import models

from shop.models import Product

from promocode.models import Promocode

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Очікує підтвердження'),
        ('processing', 'В обробці'),
        ('shipped',    'Відправлено'),
        ('delivered',  'Доставлено'),
        ('cancelled',  'Скасовано'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='покупець',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
    )
    status = models.CharField(
        'статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    total_price = models.DecimalField('загальна сума', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('дата створення', auto_now_add=True)
    updated_at = models.DateTimeField('дата оновлення', auto_now=True)

    coupon = models.ForeignKey(
        Promocode,
        verbose_name='промокод',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
    )

    discount = models.PositiveIntegerField("знижка %", default=0)

    class Meta:
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення #{self.id} — {self.get_status_display()}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='замовлення',
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
    )
    product_name = models.CharField('назва товару', max_length=100)
    price = models.DecimalField('ціна', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('кількість', default=1)

    class Meta:
        verbose_name = 'позиція замовлення'
        verbose_name_plural = 'позиції замовлення'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'

    def get_total_price(self):
        return self.price * self.quantity


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order,
        verbose_name='замовлення',
        on_delete=models.CASCADE,
        related_name='shipping_address',
    )
    first_name = models.CharField('імʼя', max_length=50)
    last_name = models.CharField('прізвище', max_length=50)
    email = models.EmailField('email')
    phone = models.CharField('телефон', max_length=20)
    city = models.CharField('місто', max_length=100)
    address = models.TextField('адреса')
    postal_code = models.CharField('поштовий індекс', max_length=20)

    class Meta:
        verbose_name = 'адреса доставки'
        verbose_name_plural = 'адреси доставки'

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.city}'