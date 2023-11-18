from rest_framework.permissions import BasePermission


# 팀 초대 기능은 팀장만 가능하므로
# 관련 권한 정의
class CanInviteTeamPermission(BasePermission):
    def has_permission(self, request, view):
        # 사용자 가져오기
        user = request.user

        # 팀장만 초대 가능
        # 팀장이다 → True / 팀장이 아니다 → False
        return user.groups.filter(name='leader').exists()
