from django.db import models

from teams.models import Team


class Board(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='소유 팀'
    )


class Column(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='보드'
    )
    title = models.TextField(verbose_name='제목')
    sequence = models.PositiveIntegerField(verbose_name='순서')
