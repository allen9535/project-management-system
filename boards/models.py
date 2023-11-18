from django.db import models

from teams.models import Team
from users.models import User


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


class Ticket(models.Model):
    TAG_CHOICES = [
        ('FE', 'Frontend'),
        ('BE', 'Backend'),
        ('D', 'Design'),
        ('QA', 'Quality Assurance'),
        ('PM', 'Project Manager'),
        ('Doc', 'Document'),
    ]

    column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        verbose_name='컬럼'
    )
    charge = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='담당자'
    )
    title = models.TextField(verbose_name='제목')
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    sequence = models.PositiveIntegerField(verbose_name='순서')
    volume = models.FloatField(verbose_name='작업량')
    ended_at = models.DateField(verbose_name='마감일')
