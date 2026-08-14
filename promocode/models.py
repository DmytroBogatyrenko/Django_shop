from django.db import models

# Create your models here.
class Promocode(models.Model):
    code = models.CharField(max_length=50, blank=False)
    value = models.IntegerField(blank=False)
    date_start = models.DateTimeField("Видано", auto_now_add=True, )
    valid_date = models.IntegerField("Валідний n-днів:", default=30)