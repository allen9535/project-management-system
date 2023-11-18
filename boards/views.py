from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError

from drf_yasg.utils import swagger_auto_schema

from config.permissions import IsTeamLeader, IsTeamMember
from teams.models import Team
from .models import Board, Column
from .serializers import ColumnSerializer, BoardSerializer

from swagger import *


# /api/v1/boards/column/create/
class ColumnCreateView(APIView):
    # 권한 설정
    # 팀의 팀장에게 권한 부여
    permission_classes = [IsAuthenticated, IsTeamLeader]

    @swagger_auto_schema(
        operation_id='컬럼 생성',
        operation_description='팀이 소유한 보드에 컬럼을 새로 생성합니다.',
        tags=['컬럼', '생성'],
        request_body=COLUMN_CREATE_PARAMETER,
        responses={
            201: SUCCESS_MESSAGE_201,
            400: ERROR_MESSAGE_400,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403
        }
    )
    def post(self, request):
        user = request.user

        # 컬럼 제목
        title = request.data.get('title')
        # 컬럼 제목은 필수값이므로 없다면 상태 코드 반환
        if title is None:
            return Response({'data': '컬럼 제목을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 사용자 그룹의 팀명으로 팀 객체 찾기
            # 현재 로그인한 사용자가 팀장으로 있는 팀이 맞는지는 권한 레벨에서 체크중
            team = Team.objects.get(
                name=user.groups.exclude(name='leader').first().name
            )
            # 팀 객체로 보드 찾기
            board = Board.objects.get(team=team)
        except ObjectDoesNotExist as error:
            return Response({'data': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 보드 내부의 컬럼을 정렬
            # 순서 필드를 내림차순으로 정렬하면 첫번째 객체의 순서는 가장 마지막 순서가 됨
            last_sequence = Column.objects.filter(
                board=board
            ).order_by('-sequence').first().sequence + 1
        except AttributeError:
            # 보드 내부에 컬럼이 없다면 순서를 1번으로 설정
            last_sequence = 1

        # 직렬화 전 데이터를 묶어줌
        column_data = {
            'board': board.id,
            'title': title,
            'sequence': last_sequence
        }

        serializer = ColumnSerializer(data=column_data)
        if serializer.is_valid():
            serializer.save()

            # 값이 유효한 경우
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        # 값이 유효하지 않은 경우
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/boards/column/update/
class ColumnUpdateView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀 구성원 전체에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='컬럼 수정',
        operation_description='컬럼 id와 기타 데이터를 받아 컬럼을 수정합니다.',
        tags=['컬럼', '수정'],
        request_body=COLUMN_UPDATE_PARAMETER,
        responses={
            200: SUCCESS_MESSAGE_200,
            400: ERROR_MESSAGE_400,
            401: ERROR_MESSAGE_401,
            404: ERROR_MESSAGE_404
        }
    )
    def put(self, request):
        if request.data.get('sequence'):
            return Response(
                {'data': '순서 변경은 시도할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        # 사용자 그룹 정보로 팀 객체 가져옴
        own_board = Board.objects.get(
            team__name=user.groups.exclude(name='leader').first().name
        )

        try:
            # 현재 사용자의 팀이 소유한 보드의 특정 컬럼을 가져옴
            column = Column.objects.get(
                id=request.data.get('column'),
                board=own_board
            )
        except (ObjectDoesNotExist, ValueError) as error:
            return Response({'data': f'{error}'}, status=status.HTTP_404_NOT_FOUND)

        # 해당하는 필드만 업데이트
        # 여기서 변경할 수 있는 값은 제목밖에 없음
        serializer = ColumnSerializer(column, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/boards/column/update/sequence/
class ColumnUpdateSequenceView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀 구성원 전체에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='컬럼 순서 수정',
        operation_description='컬럼 id와 변경된 순서를 받아 컬럼 순서를 수정합니다.',
        tags=['컬럼', '수정', '순서'],
        request_body=COLUMN_UPDATE_SEQUENCE_PARAMETER,
        responses={
            200: SUCCESS_MESSAGE_200,
            400: ERROR_MESSAGE_400,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404
        }
    )
    def put(self, request):
        user = request.user

        try:
            # 유효하지 않은 순서값을 입력했을 때를 대비한 예외처리
            update_sequence = int(request.data.get('sequence'))
        except (ValueError, TypeError) as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 사용자 그룹 정보로 팀 객체 가져옴
        own_board = Board.objects.get(
            team__name=user.groups.exclude(name='leader').first().name
        )

        try:
            # 현재 사용자의 팀이 소유한 보드의 특정 컬럼을 가져옴
            target_column = Column.objects.get(
                id=request.data.get('column'),
                board=own_board
            )
        except (ObjectDoesNotExist, ValueError) as error:
            return Response({'data': f'{error}'}, status=status.HTTP_404_NOT_FOUND)

        # 현재 보드에 있는 컬럼 총 갯수
        column_count = len(Column.objects.filter(board=own_board))
        # 만약 업데이트할 순서값이 현재 위치 그대로일 경우
        if target_column.sequence == update_sequence:
            return Response(
                {'data': '데이터 수정이 완료되었습니다.'},
                status=status.HTTP_200_OK
            )
        # 만약 업데이트할 순서값이 보드 내 전체 컬럼 갯수보다 크거나
        # 0 이하인 경우
        elif (update_sequence > column_count) or (update_sequence <= 0):
            return Response(
                {'data': '유효한 순서값을 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 트랜잭션으로 관리
            # 하나라도 문제가 발생하면 전부 롤백
            with transaction.atomic():
                # 순서를 변경할 컬럼의 순서가 원래 있던 자리보다 왼쪽으로 갈 때(순서값이 작아질 때)
                if target_column.sequence > update_sequence:
                    # 순서를 변경할 컬럼과 변경 후 가게 될 자리 사이에 있는 컬럼들을 오름차순으로 가져옴
                    before_target_columns = Column.objects.filter(
                        sequence__gte=update_sequence,
                        sequence__lt=target_column.sequence
                    ).order_by('sequence')

                    # 순회하면서 순서값들을 1씩 상승
                    for column in before_target_columns:
                        column.sequence += 1
                        column.save()

                    # 순서를 변경할 컬럼의 순서를 변경하고자 했던 순서로 변경
                    target_column.sequence = update_sequence
                    target_column.save()
                # 순서를 변경할 컬럼의 순서가 원래 있던 자리보다 오른쪽으로 갈 때(순서값이 커질 때)
                else:
                    # 순서를 변경할 컬럼과 변경 후 가게 될 자리 사이에 있는 컬럼들을 오름차순으로 가져옴
                    after_target_columns = Column.objects.filter(
                        sequence__gt=target_column.sequence,
                        sequence__lte=update_sequence
                    ).order_by('sequence')

                    # 순회하면서 순서값들을 1씩 감소
                    for column in after_target_columns:
                        column.sequence -= 1
                        column.save()

                    # 순서를 변경할 컬럼의 순서를 변경하고자 했던 순서로 변경
                    target_column.sequence = update_sequence
                    target_column.save()
        except DatabaseError as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 데이터 직렬화
        serializer = BoardSerializer(own_board)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )


# /api/v1/boards/board/list/
class BoardListView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀 구성원 전체에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='보드 목록',
        operation_description='현재 사용자의 소속 팀이 소유한 보드와 관련된 데이터를 제공합니다.',
        tags=['보드', '컬럼', '목록'],
        responses={
            200: SUCCESS_MESSAGE_200,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403
        }
    )
    def get(self, request):
        user = request.user
        # 구조상 사용자가 소속된 그룹들 중 팀장 그룹을 제외하면 팀 그룹 하나밖에 없음
        # 그 팀 그룹의 이름을 통해 팀 객체 가져옴
        user_team = Team.objects.get(
            name=user.groups.exclude(name='leader').first().name
        )

        # 가져온 팀 객체로 보드 가져옴
        board = Board.objects.get(team=user_team)
        # 시리얼라이저로 직렬화 한 후 데이터 반환
        # 컬럼명과 순서를 딕셔너리 형태로 직렬화함
        # {
        #    'team': '팀명',
        #    'column': {
        #       '컬럼id': {
        #            '컬럼제목': '컬럼 순서'
        #       },
        #       '컬럼id': {
        #            '컬럼제목': '컬럼 순서'
        #       },
        #        ...
        #     }
        # }
        serializer = BoardSerializer(board)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
