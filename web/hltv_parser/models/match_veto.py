from django.db import models
from model_utils import Choices


class MatchVeto(models.Model):
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

    number_of_action = models.IntegerField(
        verbose_name='номер выбора'
    )

    RESULT = Choices(
        (0, 'ban_team', 'Вычерк команды'),
        (1, 'ban_enemy', 'Вычерк противника'),
        (2, 'pick_team', 'Выбор команды'),
        (3, 'pick_enemy', 'Выбор противника'),
        (4, 'last', 'Крайняя'),
    )

    result = models.IntegerField(
        choices=RESULT,
    )