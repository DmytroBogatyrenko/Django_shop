from django.db import models

# Create your models here.
class Promocode(models.Model):
    code = models.CharField(max_length=50, blank=False)
    value = models.IntegerField(blank=False)
    date_start = models.DateTimeField("Видано", auto_now_add=True, )
    valid_date = models.IntegerField("Валідний n-днів:", default=30)
    max_uses = models.PositiveIntegerField("Максимум використань", default=1)
    times_used = models.PositiveIntegerField("Використано разів", default=0)
    
    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "промокоди"

    def __str__(self):
        return f"{self.code} ({self.value}%)"
    
    def is_valid(self):
        from django.utils import timezone
        import datetime

        expiry_date = self.date_start + datetime.timedelta(days=self.valid_date)

        if timezone.now() > expiry_date:
            return False  

        if self.times_used >= self.max_uses:
            return False

        return True
    