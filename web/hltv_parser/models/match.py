from django.db import models


class Match(models.Model):
    type = models.CharField(
        verbose_name='тип',
        max_length=255,
    )

    first_participant = models.ForeignKey(
        to='hltv_parser.Team',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='первый участник',
    )

    second_participant = models.ForeignKey(
        to='hltv_parser.Team',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='второй участник',
    )

    score = models.CharField(
        verbose_name='счет матча',
        max_length=255,
    )

    result = models.CharField(
        verbose_name='результат матча',
        max_length=255,
    )

    date = models.CharField(
        verbose_name='дата проведения',
        max_length=255,
    )

    tournament = models.ForeignKey(
        to='hltv_parser.Tournament',
        related_name='tournament',
        on_delete=models.deletion.CASCADE,
        verbose_name='турнир',
    )

    class Meta:
        verbose_name = 'матч'
        verbose_name_plural = 'матчи'

    # def __str__(self):
    #     return f'{self.pk} {self.name}'
