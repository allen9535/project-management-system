from celery import shared_task

from django.core.cache import cache

from teams.models import Team
from .models import Board
from .serializers import BoardSerializer


# 매일 오전 08시 50분에 자동적으로 보드를 올려놓을 수 있도록 설정
@shared_task
def preload_boards():
    # 전체 팀을 가져옴
    teams = Team.objects.all()
    # 팀을 순회하면서 각 팀의 보드를 직렬화해 캐싱
    # 컬럼이나 티켓 데이터는 보드 시리얼라이저에서 처리됨
    for team in teams:
        serializer = BoardSerializer(Board.objects.get(team=team))

        cache.set(f'{team.name}', serializer.data)
