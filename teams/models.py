from django.db import models

from users.models import User


class Team(models.Model):
    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='팀장'
    )
    name = models.CharField(max_length=20, verbose_name='팀명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')


class Teammate(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='팀'
    )
    mate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='팀원'
    )
