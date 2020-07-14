from django.db import models


class Receipt(models.Model):
    name = models.CharField(max_length=250)
    list_services = models.TextField(default='')
    full_price = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Чеки'
        verbose_name = 'Чек'
