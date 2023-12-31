from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction, DatabaseError

from drf_yasg.utils import swagger_auto_schema

from config.permissions import IsTeamLeader
from users.models import User
from users.serializers import UserSerializer
from boards.models import Board
from .models import Team
from .serializers import TeamCreateSerializer

from swagger import *


# /api/v1/teams/create/
class TeamCreateView(APIView):
    # 인증된 사용자에게만 권한 부여
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='팀 생성',
        operation_description='일반 사용자가 팀명을 입력하여 새 팀을 생성할 수 있습니다. 기존에 사용되고 있는 팀명은 사용할 수 없습니다.',
        tags=['팀', '생성'],
        request_body=TEAM_CREATE_PARAMETERS,
        responses={
            201: SUCCESS_MESSAGE_201,
            400: ERROR_MESSAGE_400,
            401: ERROR_MESSAGE_401,
            500: ERROR_MESSAGE_500
        }
    )
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
            try:
                # 트랜잭션으로 관리
                # 팀 생성 + 그룹 생성 + 사용자에게 그룹 할당 + 보드 생성을 묶었음
                # 하나라도 문제가 발생하면 전부 롤백
                with transaction.atomic():
                    # get_or_create는 튜플 형태로 (생성되거나 가져온 객체, 생성 여부) 를 반환한다
                    # 생성되거나 가져온 객체 사용
                    leader_group = Group.objects.get_or_create(
                        name='leader'
                    )[0]

                    # 기존에 다른 팀에 속해 있었는지 체크
                    is_team_mate = user.groups.exclude(name='leader').exists()
                    # 기존에 다른 팀의 팀장이었는지 체크
                    is_leader = user.groups.filter(name='leader').exists()
                    # 기존에 다른 팀의 팀장이었다면
                    if is_leader:
                        # 그 사용자의 기존 팀 그룹을 찾아서 해제
                        past_team = user.groups.exclude(name='leader').first()
                        user.groups.remove(past_team)

                        # 기존 팀의 가장 연장자에게(회원 가입일이 오래된 사용자에게) 팀장 권한 인계
                        past_team_senior = User.objects.filter(
                            groups__name=past_team.name
                        ).order_by('-date_joined').first()
                        past_team_senior.groups.add(leader_group)
                    # 팀장은 아니지만 다른 팀의 팀원이었다면
                    elif (is_leader is False) and (is_team_mate is True):
                        # 그 사용자의 기존 팀 그룹을 찾아서 해제
                        past_team = user.groups.exclude(name='leader').first()
                        user.groups.remove(past_team)

                    # 팀을 그룹 형태로 생성
                    team_group = Group.objects.create(name=team_name)

                    # 팀 생성자를 팀장 그룹에 등록
                    # 기존에 팀장이었다면 변화 없음
                    user.groups.add(leader_group)
                    # 팀 생성자를 팀 그룹에 등록
                    user.groups.add(team_group)

                    # 팀 저장
                    serializer.save()

                    # 작업 보드 생성
                    Board.objects.create(
                        team=Team.objects.get(name=serializer.data.get('name'))
                    )
            # 위 과정 처리 중 오류 발생을 대비한 예외처리
            except DatabaseError as error:
                return Response(
                    {
                        'data': f'{error}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 정상적으로 작업이 완료되었을 때
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        # 시리얼라이저의 유효성 검사 실패시
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/teams/invite/
class TeamInviteView(APIView):
    # 인증된 사용자, 팀원 초대 가능자(해당 팀의 팀장)에게만 권한 부여
    permission_classes = [IsAuthenticated, IsTeamLeader]

    @swagger_auto_schema(
        operation_id='팀 초대',
        operation_description='현재 로그인한 팀장 사용자가 다른 사용자를 팀에 초대할 수 있습니다.',
        tags=['팀', '초대'],
        request_body=TEAM_INVITE_PARAMETERS,
        responses={
            200: SUCCESS_MESSAGE_200,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404,
            423: ERROR_MESSAGE_423
        }
    )
    def post(self, request):
        user = request.user

        try:
            # 초대할 팀 객체
            # 현재 로그인한 사용자가 팀장으로 있는 팀인지 아닌지는 권한 레벨에서 판단중
            invite_team = Team.objects.get(
                name=user.groups.exclude(name='leader').first().name
            )

            # 초대할 대상 객체
            target_user = User.objects.get(
                username=request.data.get('target')
            )
        except ObjectDoesNotExist as error:
            return Response(
                {
                    'data': f'{error}'
                }, status=status.HTTP_404_NOT_FOUND
            )

        # 초대할 대상이 이미 초대 메시지를 받은 상황
        if target_user.message is not None:
            return Response(
                {
                    'data': '해당 사용자는 이미 초대를 받고 있습니다.'
                }, status=status.HTTP_423_LOCKED
            )
        # 초대할 대상이 팀장인 상황
        elif target_user.groups.filter(name='leader').exists():
            return Response(
                {
                    'data': '해당 사용자는 팀장 사용자입니다. 초대할 수 없습니다.'
                }, status=status.HTTP_423_LOCKED
            )

        # users 앱에서 초대 메시지를 분석해 팀에 가입할 수 있도록
        # 정해진 양식으로 메시지 작성
        invite_message = {
            'message': f'team:{invite_team.name},from:{user.username}'
        }

        serializer = UserSerializer(target_user, invite_message, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
