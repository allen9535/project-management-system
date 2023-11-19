from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema

from config.permissions import IsTeamLeader, IsTeamMember
from teams.models import Team
from users.models import User
from .models import Board, Column, Ticket
from .serializers import (
    ColumnSerializer,
    BoardSerializer,
    TicketSerializer
)

from swagger import *

from datetime import datetime


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
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404
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
            return Response({'data': f'{error}'}, status=status.HTTP_404_NOT_FOUND)

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

            # 변경된 보드 데이터를 캐싱
            cache.set(
                f'{team.name}',
                BoardSerializer(Board.objects.get(team=team)).data,
                60 * 60
            )

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
            403: ERROR_MESSAGE_403,
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

            # 변경된 보드 데이터를 캐싱
            cache.set(
                f'{own_board.team.name}',
                BoardSerializer(
                    Board.objects.get(team=own_board.team)
                ).data,
                60 * 60
            )

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

        # 변경된 보드 데이터를 캐싱
        cache.set(
            f'{own_board.team.name}',
            serializer.data,
            60 * 60
        )

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )


# /api/v1/boards/board/column/delete/
class ColumnDeleteView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀장에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamLeader]

    @swagger_auto_schema(
        operation_id='컬럼 삭제',
        operation_description='컬럼 id를 입력받아 해당 컬럼을 삭제합니다.',
        tags=['컬럼', '삭제'],
        request_body=COLUMN_DELETE_PARAMETER,
        responses={
            200: SUCCESS_MESSAGE_200,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404
        }
    )
    def delete(self, request):
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

        # 해당 컬럼 삭제
        column.delete()

        # 컬럼이 삭제된 다음의 보드 제공
        serializer = BoardSerializer(own_board)

        # 변경된 보드 데이터를 캐싱
        cache.set(
            f'{own_board.team.name}',
            serializer.data,
            60 * 60
        )

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# /api/v1/boards/ticket/create/
class TicketCreateView(APIView):
    # 권한 설정
    # 팀에 소속된 팀원에게 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='티켓 생성',
        operation_description='팀이 소유한 보드의 컬럼에 티켓 새로 생성합니다.',
        tags=['티켓', '생성'],
        request_body=TICKET_CREATE_PARAMETER,
        responses={
            201: SUCCESS_MESSAGE_201,
            400: ERROR_MESSAGE_400,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404
        }
    )
    def post(self, request):
        user = request.user

        try:
            # 티켓 제목
            title = request.data.get('title')
            # 컬럼 제목은 필수값이므로 없다면 오류 발생
            if title is None:
                raise ValueError

            # 태그
            tag = request.data.get('tag')
            # 티켓 모델의 TAG_CHOICES
            # 튜플을 묶은 리스트 형태
            tag_list = Ticket.TAG_CHOICES
            # 마지막 태그값
            tag_list_last = tag_list[len(tag_list) - 1]
            # 태그 순회
            for tag_data in tag_list:
                # 태그의 코드값(FE, BE ...) 과 태그명(Frontend, Backend ...)
                # 어느것도 일치하지 않고 마지막 값인 경우
                if (tag != tag_data[0]) and (tag != tag_data[1]) and (tag_data == tag_list_last):
                    return Response(
                        {'data': '잘못된 태그가 입력되었습니다.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # 태그에 일치하는 것이 있을 경우
                elif (tag == tag_data[0]) or (tag == tag_data[1]):
                    # 태그에 일치하면 DB에 저장될 값을 설정
                    tag = tag_data[0]
                    # 반복문 탈출
                    break

            # 작업량(소수)
            volume = float(request.data.get('volume'))

            # 마감일(Date): 형식을 YYYY-MM-DD 형식으로
            ended_at = datetime.strptime(
                request.data.get('ended_at'),
                '%Y-%m-%d'
            ).date()
            # 만약이 마감일이 오늘 미만(eg. 어제, 모래 ...)일 경우 오류 발생
            if ended_at < datetime.now().date():
                raise ValueError
        except (ValueError, TypeError) as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 사용자 그룹 정보로 팀 객체 가져옴
            own_board = Board.objects.get(
                team__name=user.groups.exclude(name='leader').first().name
            )

            # 입력된 컬럼 id와 보드가 일치하는 컬럼을 가져옴
            # 컬럼 id는 정상적인데 타 팀의 보드인 경우 방지
            column = Column.objects.get(
                board=own_board,
                id=int(request.data.get('column')),
            )
        except (TypeError, ValueError, ObjectDoesNotExist) as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # 컬럼 내부의 티켓을 정렬
            # 순서 필드를 내림차순으로 정렬하면 첫번째 객체는 가장 마지막에 위치하고 있는 티켓이 됨
            last_sequence = Ticket.objects.filter(
                column=column
            ).order_by('-sequence').first().sequence + 1
        except AttributeError:
            # 컬럼 내부에 티켓이 없다면 순서를 1번으로 설정
            last_sequence = 1

        charge_user = request.data.get('charge')
        if charge_user is not None:
            # 입력받은 담당자 계정명이 유효하지 않은 경우
            try:
                charge_user = User.objects.get(username=charge_user).id
            except ObjectDoesNotExist as error:
                return Response(
                    {'data': f'{error}'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # 직렬화 전 데이터를 묶어줌
        ticket_data = {
            'column': column.id,
            'charge': charge_user,
            'title': title,
            'tag': tag,
            'sequence': last_sequence,
            'volume': volume,
            'ended_at': ended_at,
        }

        serializer = TicketSerializer(data=ticket_data)
        if serializer.is_valid():
            serializer.save()

            # 변경된 보드 데이터를 캐싱
            cache.set(
                f'{own_board.team.name}',
                BoardSerializer(Board.objects.get(team=own_board.team)).data,
                60 * 60
            )

            # 값이 유효한 경우
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        # 값이 유효하지 않은 경우
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/boards/ticket/update/
class TicketUpdateView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀 구성원 전체에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='티켓 수정',
        operation_description='티켓 id와 기타 데이터를 받아 티켓을 수정합니다.',
        tags=['티켓', '수정'],
        request_body=TICKET_UPDATE_PARAMETER,
        responses={
            200: SUCCESS_MESSAGE_200,
            400: ERROR_MESSAGE_400,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404
        }
    )
    def put(self, request):
        if request.data.get('sequence'):
            return Response(
                {'data': '순서 변경은 시도할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        # request.data는 불변 객체
        # 값이 변경되어야 하는 케이스들이 있으므로 깊은 복사한 값을 사용
        request_data = request.data.copy()

        # 사용자 그룹 정보로 팀 객체 가져옴
        own_board = Board.objects.get(
            team__name=user.groups.exclude(name='leader').first().name
        )

        try:
            ended_at = request.data.get('ended_at')

            if ended_at is not None:
                ended_at = datetime.strptime(ended_at, '%Y-%m-%d').date()
                request_data['ended_at'] = ended_at
        except AssertionError as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 현재 사용자의 팀이 소유한 보드의 특정 티켓을 가져옴
            ticket = Ticket.objects.get(
                id=request.data.get('ticket'),
                column__board=own_board
            )

            # 담당자를 지정했는지 체크
            charge_username = request.data.get('charge')
            # 만약 지정해서 계정명이 넘어왔다면
            if charge_username is not None:
                # 해당 사용자 객체를 찾고
                charge = User.objects.get(username=charge_username)
                # 그 사용자가 현재 수정을 시도하는 팀의 소속인지 확인
                if charge.groups.exclude(name='leader').first().name != own_board.team.name:
                    # 수정할 티켓이 속한 팀의 팀원이 아니라면 에러 발생
                    raise ValueError

                request_data['charge'] = charge.id
        except (ObjectDoesNotExist, ValueError, AttributeError) as error:
            return Response({'data': f'{error}'}, status=status.HTTP_404_NOT_FOUND)

        # 해당하는 필드만 업데이트
        serializer = TicketSerializer(ticket, request_data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # 변경된 보드 데이터를 캐싱
            cache.set(
                f'{own_board.team.name}',
                BoardSerializer(Board.objects.get(team=own_board.team)).data,
                60 * 60
            )

            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/boards/ticket/update/sequence/
class TicketUpdateSequenceView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀 구성원 전체에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='티켓 순서 수정',
        operation_description='변경할 컬럼 id와 티켓 id를 받아 티켓 순서를 수정합니다.',
        tags=['티켓', '수정', '순서'],
        request_body=TICKET_UPDATE_SEQUENCE_PARAMETER,
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

        # 사용자 그룹 정보로 팀 객체 가져옴
        own_board = Board.objects.get(
            team__name=user.groups.exclude(name='leader').first().name
        )

        try:
            # 현재 사용자의 팀이 소유한 보드의 순서를 변경할 티켓을 가져옴
            target_ticket = Ticket.objects.get(
                id=request.data.get('ticket'),
                column__board=own_board
            )
        except (ObjectDoesNotExist, ValueError) as error:
            return Response({'data': f'{error}'}, status=status.HTTP_404_NOT_FOUND)

        # 유효하지 않은 순서값을 입력했을 때를 대비한 예외처리
        try:
            update_column_sequence = int(request.data.get('column_sequence'))
            update_ticket_sequence = int(request.data.get('ticket_sequence'))
        except (ValueError, TypeError) as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 만약 컬럼 단위의 변경이 없다면
            if update_column_sequence == target_ticket.column.sequence:
                # 해당 컬럼의 티켓 갯수
                ticket_count = len(
                    Ticket.objects.filter(column=target_ticket.column)
                )

                # 티켓 단위의 변경도 없다면
                if target_ticket.sequence == update_ticket_sequence:
                    return Response(
                        {'data': '데이터 수정이 완료되었습니다.'},
                        status=status.HTTP_200_OK
                    )
                # 현재 컬럼의 전체 티켓 수보다 큰 값을 받았거나 0 이하의 값을 받았을 경우
                elif (update_ticket_sequence > ticket_count) or (update_ticket_sequence <= 0):
                    return Response(
                        {'data': '유효한 순서값을 입력해주세요.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 트랜잭션으로 관리
                # 하나라도 문제가 발생하면 전부 롤백
                with transaction.atomic():
                    # 순서를 변경할 티켓의 순서가 원래 있던 자리보다 왼쪽으로 갈 때(순서값이 작아질 때)
                    if target_ticket.sequence > update_ticket_sequence:
                        # 순서를 변경할 티켓과 변경 후 가게 될 자리 사이에 있는 티켓들을 오름차순으로 가져옴
                        before_target_tickets = Ticket.objects.filter(
                            column=target_ticket.column,
                            sequence__gte=update_ticket_sequence,
                            sequence__lt=target_ticket.sequence
                        ).order_by('sequence')

                        # 순회하면서 순서값들을 1씩 상승
                        for ticket in before_target_tickets:
                            ticket.sequence += 1
                            ticket.save()

                        target_ticket.sequence = update_ticket_sequence
                        target_ticket.save()
                    # 순서를 변경할 컬럼의 순서가 원래 있던 자리보다 오른쪽으로 갈 때(순서값이 커질 때)
                    else:
                        # 순서를 변경할 컬럼과 변경 후 가게 될 자리 사이에 있는 컬럼들을 오름차순으로 가져옴
                        after_target_tickets = Ticket.objects.filter(
                            column=target_ticket.column,
                            sequence__gt=target_ticket.sequence,
                            sequence__lte=update_ticket_sequence
                        ).order_by('sequence')

                        # 순회하면서 순서값들을 1씩 감소
                        for ticket in after_target_tickets:
                            ticket.sequence -= 1
                            ticket.save()

                        # 순서를 변경할 티켓의 순서를 변경하고자 했던 순서로 변경
                        target_ticket.sequence = update_ticket_sequence
                        target_ticket.save()
            # 컬럼 단위의 변경이 있다면
            else:
                try:
                    destination_column = Column.objects.get(
                        board=own_board,
                        sequence=update_column_sequence
                    )
                except ObjectDoesNotExist as error:
                    return Response(
                        {'data': f'{error}'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # 도착할 컬럼의, 티켓 데이터가 들어갈 순서값 이상의 데이터를 오름차순으로
                destination_column_tickets = Ticket.objects.filter(
                    column=destination_column,
                    sequence__gte=update_ticket_sequence
                ).order_by('sequence')

                # 원래 있던 컬럼의 티켓 데이터를 오름차순으로
                past_column_tickets = Ticket.objects.filter(
                    column=target_ticket.column
                ).order_by('sequence')

                # 트랜잭션으로 관리
                # 하나라도 문제가 발생하면 전부 롤백
                with transaction.atomic():
                    # 순회 돌면서 순서를 수정할 티켓이 들어갈 자리 이상의 순서값을 가진 티켓들의 순서값을 전부 +1
                    for ticket in destination_column_tickets:
                        ticket.sequence += 1
                        ticket.save()

                    # 순서를 수정할 티켓값의 컬럼값과 순서값을 수정
                    target_ticket.column = destination_column
                    target_ticket.sequence = update_ticket_sequence
                    target_ticket.save()

                    # 원래 있던 컬럼의 티켓들을 순회하면서 순서 수정
                    for i in range(len(past_column_tickets)):
                        past_column_tickets[i].sequence = i + 1
                        past_column_tickets[i].save()
        except DatabaseError as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 직렬화
        serializer = BoardSerializer(own_board)

        # 변경된 보드 데이터를 캐싱
        cache.set(
            f'{own_board.team.name}',
            serializer.data,
            60 * 60
        )

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )


# /api/v1/boards/board/ticket/delete/
class TicketDeleteView(APIView):
    # 권한 설정
    # 인증된 사용자, 팀장에 권한 부여
    permission_classes = [IsAuthenticated, IsTeamMember]

    @swagger_auto_schema(
        operation_id='티켓 삭제',
        operation_description='티켓 id를 입력받아 해당 티켓을 삭제합니다.',
        tags=['컬럼', '삭제'],
        request_body=TICKET_DELETE_PARAMETER,
        responses={
            200: SUCCESS_MESSAGE_200,
            401: ERROR_MESSAGE_401,
            403: ERROR_MESSAGE_403,
            404: ERROR_MESSAGE_404
        }
    )
    def delete(self, request):
        user = request.user

        # 사용자 그룹 정보로 팀 객체 가져옴
        own_board = Board.objects.get(
            team__name=user.groups.exclude(name='leader').first().name
        )

        try:
            # 현재 사용자의 팀이 소유한 보드의 특정 티켓을 가져옴
            ticket = Ticket.objects.get(
                id=int(request.data.get('ticket')),
                column__board=own_board
            )
        except (ObjectDoesNotExist, ValueError, TypeError) as error:
            return Response({'data': f'{error}'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                # 해당 컬럼 삭제
                ticket.delete()

                # 남은 티켓들의 순서 정리
                remain_tickets = Ticket.objects.filter(
                    column=ticket.column
                ).order_by('sequence')
                for i in range(len(remain_tickets)):
                    remain_tickets[i].sequence = (i + 1)
        except DatabaseError as error:
            return Response(
                {'data': f'{error}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 티켓이 삭제된 다음의 보드 제공
        serializer = BoardSerializer(own_board)

        # 변경된 보드 데이터를 캐싱
        cache.set(
            f'{own_board.team.name}',
            serializer.data,
            60 * 60
        )

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


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

        # 팀 이름으로 저장된 보드 데이터가 있을 경우 해당 데이터 반환
        cached_board = cache.get(f'{user_team.name}')
        if cached_board:
            return Response({'data': cached_board}, status=status.HTTP_200_OK)

        # 가져온 팀 객체로 보드 가져옴
        board = Board.objects.get(team=user_team)
        # 시리얼라이저로 직렬화 한 후 데이터 반환
        # 컬럼명과 순서를 딕셔너리 형태로 직렬화함
        serializer = BoardSerializer(board)

        # 핵심 기능이므로 캐싱해둠
        # 만료 시간은 1시간
        cache.set(f'{user_team.name}', serializer.data, 60 * 60)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
