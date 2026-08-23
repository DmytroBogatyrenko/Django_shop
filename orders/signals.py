from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Order


@receiver(pre_save, sender=Order)
def track_status_change(sender, instance, **kwargs):

    if not instance.pk:
        return

    try:
        old = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    if old.status != instance.status:
        from .models import OrderStatusHistory
        OrderStatusHistory.objects.create(
            order=instance,
            old_status=old.status,
            new_status=instance.status,
        )