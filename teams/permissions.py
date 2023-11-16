from rest_framework.permissions import BasePermission


class CanInviteTeamPermission(BasePermission):
    def has_permission(self, request, view):
        # 사용자 가져오기
        user = request.user

        # 팀장만 초대 가능
        # 팀장이다 → True / 팀장이 아니다 → False
        return user.groups.filter(name='leader').exists()
