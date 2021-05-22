from django.db import models


class MatchMap(models.Model):
    match = models.ForeignKey(
        to='hltv_parser.Match',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='матч',
    )

    map = models.ForeignKey(
        to='hltv_parser.Map',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='карта',
    )

    datetime = models.DateField(
        verbose_name='дата'
    )

    score = models.CharField(
        verbose_name='счет карты',
        max_length=255,
    )

    result = models.CharField(
        verbose_name='результат карты',
        max_length=255,
    )

    veto = models.ForeignKey(
        to='hltv_parser.MatchVeto',
        related_name='+',
        on_delete=models.deletion.CASCADE,
        verbose_name='вето',
    )
