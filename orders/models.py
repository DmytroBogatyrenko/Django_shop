import datetime
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from shop.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Очікує підтвердження'),
        ('paid',       'Оплачено'),
        ('processing', 'В обробці'),
        ('shipped',    'Відправлено'),
        ('delivered',  'Доставлено'),
        ('cancelled',  'Скасовано'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Готівкою при отриманні'),
        ('card', 'Оплата карткою онлайн'),
        ('bank', 'Банківський переказ'),
    ]

    CANCEL_HOURS = 24

    order_number = models.CharField(
        'номер замовлення', max_length=32, unique=True, blank=True,
    )

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
    payment_method = models.CharField(
        'спосіб оплати', max_length=20, choices=PAYMENT_CHOICES, default='cash',
    )
    notes = models.TextField('коментар до замовлення', blank=True)
    total_price = models.DecimalField(
        'загальна сума', max_digits=10, decimal_places=2, default=0
    )

    estimated_delivery = models.DateField(
        'розрахункова дата доставки', null=True, blank=True
    )

    coupon = models.ForeignKey(
        'promocode.Promocode',
        verbose_name='промокод',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders',
    )
    discount = models.PositiveIntegerField('знижка %', default=0)

    created_at = models.DateTimeField('дата створення', auto_now_add=True)
    updated_at = models.DateTimeField('дата оновлення', auto_now=True)

    class Meta:
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення #{self.id} — {self.get_status_display()}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        if not self.pk and not self.estimated_delivery:
            self.estimated_delivery = (
                timezone.now().date() + datetime.timedelta(days=5)
            )
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_order_number():
        """Номер виду ORD-20260727-1A2B3C4D — читабельний і практично унікальний."""
        return f'ORD-{timezone.localdate():%Y%m%d}-{uuid.uuid4().hex[:8].upper()}'

    @property
    def is_paid(self):
        return self.status not in ('pending', 'cancelled')

    @property
    def requires_online_payment(self):
        return self.payment_method == 'card' and self.status == 'pending'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def can_be_cancelled(self):
        if self.status in ('shipped', 'delivered', 'cancelled'):
            return False
        hours_since_creation = (timezone.now() - self.created_at).total_seconds() / 3600
        return hours_since_creation <= self.CANCEL_HOURS

    def get_status_timeline(self):
        all_statuses = ['pending', 'processing', 'shipped', 'delivered']
        if self.status == 'cancelled':
            return [{'key': 'cancelled', 'label': 'Скасовано', 'done': True}]

        current_index = 0
        for i, s in enumerate(all_statuses):
            if s == self.status:
                current_index = i

        return [
            {
                'key': s,
                'label': dict(self.STATUS_CHOICES).get(s, s),
                'done': i <= current_index,
            }
            for i, s in enumerate(all_statuses)
        ]


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history',
    )
    old_status = models.CharField('попередній статус', max_length=20)
    new_status = models.CharField('новий статус', max_length=20)
    changed_at = models.DateTimeField('дата зміни', auto_now_add=True)
    comment = models.TextField('коментар', blank=True)

    class Meta:
        verbose_name = 'зміна статусу'
        verbose_name_plural = 'зміни статусів'
        ordering = ['-changed_at']

    def __str__(self):
        return f'#{self.order.id}: {self.old_status} → {self.new_status}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name='замовлення',
        on_delete=models.CASCADE, related_name='items',
    )
    product = models.ForeignKey(
        Product, verbose_name='товар',
        on_delete=models.SET_NULL, null=True, related_name='order_items',
    )
    product_name = models.CharField('назва товару', max_length=100)
    price        = models.DecimalField('ціна', max_digits=10, decimal_places=2)
    quantity     = models.PositiveIntegerField('кількість', default=1)

    class Meta:
        verbose_name = 'позиція замовлення'
        verbose_name_plural = 'позиції замовлення'

    def __str__(self):
        return f'{self.product_name} × {self.quantity}'

    def get_total_price(self):
        return self.price * self.quantity


class ShippingAddress(models.Model):
    order       = models.OneToOneField(
        Order, verbose_name='замовлення',
        on_delete=models.CASCADE, related_name='shipping_address',
    )
    first_name  = models.CharField('імʼя', max_length=50)
    last_name   = models.CharField('прізвище', max_length=50)
    email       = models.EmailField('email')
    phone       = models.CharField('телефон', max_length=20)
    city        = models.CharField('місто', max_length=100)
    address     = models.TextField('адреса')
    postal_code = models.CharField('поштовий індекс', max_length=20)

    class Meta:
        verbose_name = 'адреса доставки'
        verbose_name_plural = 'адреси доставки'

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.city}'
