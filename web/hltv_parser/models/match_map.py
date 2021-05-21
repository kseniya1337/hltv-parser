from django.db import models


class MatchMap(models.Model):
    match = models.ForeignKey(
        to='hltv_parser.Match',
        related_name='match',
        on_delete=models.deletion.SET_NULL,
        verbose_name='матч',
    )

    map = models.ForeignKey(
        to='hltv_parser.Map',
        related_name='map',
        on_delete=models.deletion.SET_NULL,
        verbose_name='карта',
    )

    datetime = models.DateField(
        verbose_name='дата'
    )

    score = models.CharField(
        verbose_name='счет карты'
    )

    result = models.CharField(
        verbose_name='результат карты'
    )

    veto = models.ForeignKey(
        to='hltv_parser.Veto',
        related_name='veto',
        on_delete=models.deletion.SET_NULL,
        verbose_name='вето',
    )
