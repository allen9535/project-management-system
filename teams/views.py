from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import Group

from django.db import transaction, DatabaseError

from drf_yasg.utils import swagger_auto_schema

from .serializers import TeamCreateSerializer
from .permissions import CanCreateTeamPermission


class TeamCreateView(APIView):
    # 인증된 사용자,
    # 팀 생성 가능자(리더가 아닌 사용자)에게만 권한 부여
    permission_classes = [IsAuthenticated, CanCreateTeamPermission]

    def post(self, request):
        # 사용자 데이터
        user = request.user
        # 입력된 팀명
        team_name = request.data.get('name')

        # 사용자 데이터와 팀명 데이터 하나로 묶기
        team_data = {
            # 사용자 객체가 아니라 id 필드만
            'leader': user.id,
            'name': team_name
        }

        serializer = TeamCreateSerializer(data=team_data)
        if serializer.is_valid():
            # get_or_create는 튜플 형태로
            # (생성되거나 생성한 객체, 생성 여부) 를 반환한다
            # 사실 is_created의 경우 사용할 일이 없음
            leader_group, is_created = Group.objects.get_or_create(
                name='leader'
            )

            try:
                # 트랜잭션으로 관리
                # 그룹 만들기 + 사용자에게 그룹 할당하기 + 팀 생성하기를 묶었음
                # 하나라도 문제가 발생하면 전부 롤백
                with transaction.atomic():
                    team_group = Group.objects.create(name=team_name)

                    user.groups.add(team_group)
                    user.groups.add(leader_group)

                    serializer.save()
            # 위 과정 처리 중 오류 발생을 대비한 예외처리
            except DatabaseError as error:
                return Response({'data': f'{error}'}, status=status.HTTP_418_IM_A_TEAPOT)

            # 정상적으로 작업이 완료되었을 때
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        # 시리얼라이저의 유효성 검사 실패시
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
