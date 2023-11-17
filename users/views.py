from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db import transaction, DatabaseError

from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer
from swagger import USER_REGISTER_PARAMETERS, LOGIN_PARAMETERS


# /api/v1/users/register/
class UserRegisterView(APIView):
    @swagger_auto_schema(
        operation_id='회원가입',
        operation_description='계정명과 비밀번호를 통해 회원가입을 진행합니다.',
        tags=['사용자', '생성', '인증'],
        request_body=USER_REGISTER_PARAMETERS,
        responses={
            201: '정상적으로 회원가입이 완료되었습니다.',
            400: '회원가입에 실패했습니다. 입력된 값이 잘못되었습니다. 상세한 내용은 에러 메시지를 확인해주세요.'
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        # 유효성 검사에서 문제가 없을 경우
        if serializer.is_valid():
            serializer.save()

            return Response({'data': '회원가입이 완료되었습니다.'}, status=status.HTTP_201_CREATED)

        # 유효성 검사에서 문제가 발생했을 경우
        # 해당 문제에 대한 메시지와 상태 코드 400 반환
        return Response({'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/users/login/
class LoginView(APIView):
    @swagger_auto_schema(
        operation_id='로그인',
        operation_description='계정명과 비밀번호를 활용하여 로그인을 진행합니다.',
        tags=['사용자', '로그인', '인증'],
        request_body=LOGIN_PARAMETERS,
        responses={
            200: '정상적으로 로그인이 완료되었습니다.',
            400: '로그인에 실패했습니다. 필수값이 입력되지 않았습니다.',
            404: '로그인에 실패했습니다. 해당하는 사용자를 찾지 못했습니다.'
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # 계정명과 비밀번호는 필수값, 두 값이 모두 있어야 함
        if (username is None) or (password is None):
            return Response({'data': '필수값(계정명, 비밀번호)가 입력되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당하는 사용자가 있으면 User 객체를, 없으면 None 반환
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'data': '해당하는 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 액세스 토큰과 리프레시 토큰을 함께 발급
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 리프레시 토큰의 보안과 성능을 위해 Redis에 캐시 데이터로 저장
        # 리프레시 토큰의 만료 기간을 매우 길게 잡았으므로(2주),
        # 만료기간을 이에 맞춤(1,209,600초)
        # 액세스 토큰을 키 값으로 리프레시 토큰을 저장함
        cache.set(f'{access_token}', refresh_token, 60 * 60 * 24 * 14)

        return Response({'data': '로그인이 완료되었습니다', 'access': access_token}, status=status.HTTP_200_OK)


# /api/v1/users/logout/
class LogoutView(APIView):
    # 권한으로 인증을 요구
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='로그아웃',
        operation_description='액세스 토큰을 통해 캐시에 저장된 리프레시 토큰을 블랙리스트에 등록하여 재사용을 막습니다. 액세스 토큰 삭제는 이루어지지 않습니다.',
        tags=['사용자', '로그아웃', '인증'],
        responses={
            200: '정상적으로 로그아웃이 완료되었습니다.',
            202: '로그아웃은 성공했습니다. 그러나 정상적으로 로그아웃이 처리되지 않았을 수 있습니다. 에러 메시지를 확인해주세요.',
            401: '인증되지 않은 사용자는 사용할 수 없습니다.'
        }
    )
    def post(self, request):
        # 요청 헤더에서 Authorization을 가져온 다음('Bearer Token')
        # 공백을 기준으로 나누고(['Bearer', 'Token'])
        # 토큰만 가져옴
        access_token = request.headers.get('Authorization').split()[1]
        # 액세스 토큰을 키 값으로 리프레시 토큰을 찾음
        # 만약 없으면 None 값이 됨
        refresh_token = cache.get(f'{access_token}')

        if refresh_token is None:
            return Response({'data': '로그아웃이 완료되었습니다. 그러나 리프레시 토큰이 정상적으로 처리되지 않았을 수 있습니다.'}, status=status.HTTP_202_ACCEPTED)

        try:
            # 리프레시 토큰을 문자열에서 리프레시 토큰 객체로 형변환
            token = RefreshToken(refresh_token)
            # 리프레시 토큰을 블랙리스트에 등록하여 재사용 차단
            token.blacklist()

            # 캐시 데이터에서 리프레시 토큰 삭제
            cache.delete(f'{access_token}')

            return Response({'data': '로그아웃이 완료되었습니다.'}, status=status.HTTP_200_OK)
        # 리프레시 토큰 처리 중 발생할 수 있는 예외를 처리
        except (InvalidToken, TokenError) as error:
            return Response({'data': f'{error}'}, status=status.HTTP_202_ACCEPTED)


# /api/v1/users/invite/
class UserInviteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='초대 메시지 확인',
        operation_description='사용자에게 온 초대 메시지를 확인합니다.',
        tags=['사용자', '팀', '초대'],
        responses={
            200: '사용자에게 온 초대 메시지 검색이 성공적으로 완료되었습니다.',
            204: '사용자에게 온 초대 메시지가 없습니다.',
            401: '인증되지 않은 사용자는 사용할 수 없습니다.'
        }
    )
    def get(self, request):
        user = request.user

        # 현재 사용자에게 온 메시지가 없을 경우
        if user.message is None:
            return Response(
                {'data': '초대받은 내용이 없습니다.'}, status=status.HTTP_204_NO_CONTENT
            )

        # 팀 메시지는 정해진 양식으로 보내고 있으므로
        # 팀명과 초대자를 가져옴
        # user.message → team:팀명,from:팀장

        # 팀명
        invite_team = user.message.split(',')[0].split(':')[1]
        # 팀장
        invite_from = user.message.split(',')[1].split(':')[1]
        # 출력할 초대 메시지
        invite_message = f'{invite_team} 팀의 {invite_from}팀장에게서 초대를 받았습니다.'

        return Response(
            {'date': invite_message}, status=status.HTTP_200_OK
        )


# /api/v1/users/invite/accept/
class UserInviteAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='초대 메시지 수락',
        operation_description='사용자에게 온 초대 메시지를 수락합니다.',
        tags=['사용자', '팀', '초대'],
        responses={
            202: '초대 메시지 수락이 성공적으로 완료되었습니다.',
            204: '사용자에게 온 초대 메시지가 없습니다.',
            401: '인증되지 않은 사용자는 사용할 수 없습니다.',
            500: '요청을 처리하던 중 서버에 문제가 발생했습니다.'
        }
    )
    def post(self, request):
        user = request.user

        # 팀 메시지는 정해진 양식으로 보내고 있으므로
        # split으로 팀명만 가져옴
        # user.message → team:팀명,from:팀장

        try:
            # 메시지를 분석해서 팀명 가져옴
            team_name = user.message.split(',')[0].split(':')[1]
        # 해당 사용자에게 초대 메시지가 없을 경우를 대비한 예외처리
        except AttributeError as error:
            return Response(
                {'data': '해당 사용자는 초대 메시지가 없습니다.'}, status=status.HTTP_204_NO_CONTENT
            )

        # 그룹 객체
        team = Group.objects.get(name=team_name)

        try:
            # 트랜잭션으로 관리
            # 사용자에게 그룹 할당하기 + 사용자의 메시지 필드 비우기
            # + 만약 이미 팀이 있다면 그 팀으로 옮기기
            # 하나라도 문제가 발생하면 전부 롤백
            with transaction.atomic():
                # 현재 사용자가 팀장 그룹 이외의 그룹에 소속되어 있다면 특정 팀에 소속된 것
                if user.groups.exclude(name='leader').exists():
                    # 그 팀의 그룹 객체
                    joined = user.groups.exclude(name='leader').first()
                    # 현재 사용자에게서 팀 그룹 삭제
                    user.groups.remove(joined)

                # 현재 사용자를 메시지에 있던 팀 그룹에 추가
                user.groups.add(team)

                # 현재 사용자의 메시지 필드를 비움
                user.message = None
                # 위 과정이 전부 정상적으로 진행되었다면 저장
                user.save()
        # 트랜잭션에서 에러가 발생할 경우를 대비한 예외 처리
        except DatabaseError as error:
            return Response(
                {'data': f'{error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'data': f'{team_name} 팀의 초대를 수락하셨습니다.'}, status=status.HTTP_202_ACCEPTED
        )
