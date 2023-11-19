from rest_framework.permissions import BasePermission

from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from teams.models import Team


# 팀장에게 권한을 부여
class IsTeamLeader(BasePermission):
    def has_permission(self, request, view):
        # 사용자 가져오기
        user = request.user

        try:
            # 팀 가져오기
            team = Team.objects.get(
                name=user.groups.exclude(name='leader').first().name
            )
        # 만약 팀에 소속되지 않은 상황이라면 상태 코드 반환
        except ObjectDoesNotExist as error:
            return Response({'data': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 팀의 팀장만 초대 가능
        # 해당 팀의 팀장이다 → True / 그 외 → False
        return (user.groups.filter(name='leader').exists()) and (team.leader == user)


# 팀의 구성원 전체에 권한을 부여
class IsTeamMember(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # 팀장 이외의 그룹은 모두 팀 그룹이므로
        return user.groups.exclude(name='leader').exists()
