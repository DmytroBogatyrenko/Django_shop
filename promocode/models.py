from django.db import models
from django.utils import timezone
import datetime


class Promocode(models.Model):
    code = models.CharField("Промокод", max_length=50, unique=True, blank=False)
    value = models.IntegerField("Знижка (%)", blank=False)
    date_start = models.DateTimeField("Видано", auto_now_add=True)
    valid_date = models.IntegerField("Валідний (днів)", default=30)
    max_uses = models.PositiveIntegerField("Максимум використань", default=1)
    times_used = models.PositiveIntegerField("Використано разів", default=0)

    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "промокоди"

    def __str__(self):
        return f"{self.code} ({self.value}%)"

    def is_valid(self):
        expiry_date = self.date_start + datetime.timedelta(days=self.valid_date)
        if timezone.now() > expiry_date:
            return False
        if self.times_used >= self.max_uses:
            return False
        return True