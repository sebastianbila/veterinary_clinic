from django.db import models


class ClinicServices(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Послуги Клiнiки"


class CategoryServices(models.Model):
    service = models.ForeignKey(ClinicServices,
                                on_delete=models.DO_NOTHING,
                                related_name='category_service')
    title = models.CharField(max_length=250)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Категорії Послуг"


class Recipe(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Рецепти"


