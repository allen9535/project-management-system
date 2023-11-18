from rest_framework.permissions import BasePermission

from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from teams.models import Team


# 컬럼 생성은 해당 팀의 팀장만 가능함
# 관련 권한 정의
class CanCreateColumn(BasePermission):
    def has_permission(self, request, view):
        # 사용자 가져오기
        user = request.user

        try:
            # 팀 가져오기
            team = Team.objects.get(
                name=request.data.get('team')
            )
        # 만약 팀명을 입력하지 않은 상황이라면 상태 코드 반환
        except ObjectDoesNotExist as error:
            return Response({'data': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 팀의 팀장만 컬럼 생성 가능
        # 해당 팀의 팀장이다 → True / 그 외 → False
        return (user.groups.filter(name='leader').exists()) and (team.leader == user)
