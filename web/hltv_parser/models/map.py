from django.db import models


class Map(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=255,
    )


    class Meta:
        verbose_name = 'карта'
        verbose_name_plural = 'карты'

    def __str__(self):
        return f'{self.pk} {self.name}'
