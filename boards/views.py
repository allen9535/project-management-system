from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from drf_yasg.utils import swagger_auto_schema

from teams.models import Team
from .permissions import CanCreateColumn, CanReadBoardList
from .models import Board, Column
from .serializers import ColumnSerializer, BoardSerializer

from swagger import COLUMN_CREATE_PARAMETER


# /api/v1/boards/column/create/
class ColumnCreateView(APIView):
    # 권한 설정
    # 인증된 사용자, 컬럼 생성 가능한 사용자에게만 권한 부여
    # 컬럼 생성 가능한 사용자: 요청으로 넘어온 팀의 팀장
    permission_classes = [IsAuthenticated, CanCreateColumn]

    @swagger_auto_schema(
        operation_id='컬럼 생성',
        operation_description='팀이 소유한 보드에 컬럼을 새로 생성합니다.',
        tags=['컬럼', '생성'],
        request_body=COLUMN_CREATE_PARAMETER,
        responses={
            201: '성공적으로 컬럼을 생성했습니다.',
            400: '입력값 오류. 컬럼 생성에 실패했습니다. 잘못된 값이 입력되었습니다.',
            401: '인증 오류. 인증되지 않은 사용자입니다.',
            403: '권한 오류. 팀장이 자기 보드에만 컬럼을 생성할 수 있습니다.'
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
            # 요청에 담긴 팀명으로 팀 객체 찾기
            # 현재 로그인한 사용자가 팀장으로 있는 팀이 맞는지는 권한 레벨에서 체크중
            team = Team.objects.get(
                name=request.data.get('team')
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

        # 값이 유효한 경우
        serializer = ColumnSerializer(data=column_data)
        if serializer.is_valid():
            serializer.save()

            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        # 값이 유효하지 않은 경우
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/boards/board/list/
class BoardListView(APIView):
    # 권한 설정
    # 인증된 사용자, 보드 내용 확인 가능한 사용자에게만 권한 부여
    # 보드 내용 확인 가능한 사용자: 요청으로 넘어온 팀의 팀장 또는 팀원
    permission_classes = [IsAuthenticated, CanReadBoardList]

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
        #       '컬럼명': 순서,
        #       '컬럼명': 순서,
        #        ...
        #     }
        # }
        serializer = BoardSerializer(board)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
