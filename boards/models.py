from django.db import models

from teams.models import Team


class Board(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='소유 팀'
    )
