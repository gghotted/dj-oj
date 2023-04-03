from core.models import BaseModel
from django.db import models


class Rank(BaseModel):
    user = models.OneToOneField(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='rank',
        verbose_name='유저',
    )
    rank = models.PositiveBigIntegerField(
        verbose_name='랭크',
        null=True,
    )
    score = models.PositiveIntegerField(
        verbose_name='점수',
        null=True,
    )
