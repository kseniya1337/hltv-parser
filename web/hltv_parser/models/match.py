from django.db import models


class Match(models.Model):
    hltv_id = models.IntegerField(
        verbose_name='id матча на hltv'
    )
    match_type = models.CharField(
        verbose_name='тип',
        max_length=255,
    )

    first_team = models.ForeignKey(
        to='hltv_parser.Team',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='первая команда',
    )

    second_team = models.ForeignKey(
        to='hltv_parser.Team',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='вторая команда',
    )

    first_team_score = models.IntegerField(
        verbose_name='результат первой команды'
    )

    second_team_score = models.IntegerField(
        verbose_name='результат второй команды'
    )

    match_date = models.CharField(
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
