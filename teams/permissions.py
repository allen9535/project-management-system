from rest_framework.permissions import BasePermission


# 이미 팀장인 사용자는 팀을 생성할 수 없게 하는 권한
class CanCreateTeamPermission(BasePermission):
    def has_permission(self, request, view):
        # 사용자 가져오기
        user = request.user

        # 사용자 그룹 중 leader 가 있을 경우 → False 반환
        # 권한 X
        if user.groups.filter(name='leader').exists():
            return False

        # 사용자 그룹 중 leader 가 없을 경우 → True 반환
        # 권한 O
        return True
