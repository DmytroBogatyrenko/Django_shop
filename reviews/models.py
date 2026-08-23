from django.db import models

# Create your models here.

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from shop.models import Product


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='покупець',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='товар',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    rating = models.PositiveSmallIntegerField(
        'рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField('текст відгуку')
    created_at = models.DateTimeField('дата', auto_now_add=True)

    is_verified_purchase = models.BooleanField(
        'підтверджена покупка', default=False
    )
    is_approved = models.BooleanField('схвалено', default=False)

    class Meta:
        verbose_name = 'відгук'
        verbose_name_plural = 'відгуки'
        ordering = ['-created_at']
        unique_together = [['user', 'product']]

    def __str__(self):
        return f'{self.user.username} → {self.product.name} ({self.rating}★)'

    def save(self, *args, **kwargs):

        from orders.models import OrderItem
        self.is_verified_purchase = OrderItem.objects.filter(
            order__user=self.user,
            product=self.product,
        ).exists()
        super().save(*args, **kwargs)
