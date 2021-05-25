from django.db import models


class Team(models.Model):
    hltv_id = models.IntegerField(
        verbose_name='id команды на hltv',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='название',
    )

    # world_ranking = models.IntegerField(
    #     verbose_name='мировой рейтинг',
    # )

    #
    # logo = models.ImageField(
    #     verbose_name='логотип'
    # )

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'

    def __str__(self):
        return f'{self.pk} {self.name}'
