from django.db import models


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='название',
    )

    world_ranking = models.IntegerField(
        verbose_name='мировой рейтинг',
    )

    matches = models.ForeignKey(
        to='hltv_parser.Match',
        related_name='matches',
        on_delete=models.deletion.SET_NULL,
        null=True,
        blank=True,
        verbose_name='матчи',
    )
    logo = models.ImageField(
        verbose_name='логотип'
    )

    class Meta:
        verbose_name = 'команда'
        verbose_name_plural = 'команды'

    def __str__(self):
        return f'{self.pk} {self.name}'
