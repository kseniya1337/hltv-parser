from django.db import models


class Tournament(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='название',
    )

    date = models.CharField(
        verbose_name='дата проведения',
        max_length=255,
    )

    logo = models.ImageField(
        verbose_name='логотип'
    )

    class Meta:
        verbose_name = 'турнир'
        verbose_name_plural = 'турниры'

    def __str__(self):
        return f'{self.pk} {self.name}'

