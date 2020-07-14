from django.db import models


class ClinicPatients(models.Model):
    nickname = models.CharField(max_length=150)
    image = models.ImageField(upload_to='patients')
    description = models.TextField()
    owner = models.CharField(max_length=150, default='')
    patient_type = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = "Пацієнти"
        verbose_name = "Пацієнта"
        app_label = 'patients'
