from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


from django.contrib.auth import authenticate
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer
from swagger import *


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

            return Response(
                {
                    'message': '회원가입이 완료되었습니다.'
                }, status=status.HTTP_201_CREATED
            )

        # 유효성 검사에서 문제가 발생했을 경우
        # 해당 문제에 대한 메시지와 상태 코드 400 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(
                {
                    'message': '필수값(계정명, 비밀번호)가 입력되지 않았습니다.'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        # 해당하는 사용자가 있으면 User 객체를, 없으면 None 반환
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {
                    'message': '해당하는 사용자를 찾을 수 없습니다.'
                }, status=status.HTTP_404_NOT_FOUND
            )

        # 액세스 토큰과 리프레시 토큰을 함께 발급
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 리프레시 토큰의 보안과 성능을 위해 Redis에 캐시 데이터로 저장
        # 리프레시 토큰의 만료 기간을 매우 길게 잡았으므로(2주),
        # 만료기간을 이에 맞춤(1,209,600초)
        # 액세스 토큰을 키 값으로 리프레시 토큰을 저장함
        cache.set(f'{access_token}', refresh_token, 60 * 60 * 24 * 14)

        return Response(
            {
                'message': '로그인이 완료되었습니다',
                'access': access_token
            }, status=status.HTTP_200_OK
        )


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
            202: '로그아웃은 성공했습니다. 그러나 정상적으로 로그아웃이 처리되지 않았을 수 있습니다. 에러 메시지를 확인해주세요.'
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
            return Response(
                {
                    'message': '로그아웃이 완료되었습니다. 그러나 리프레시 토큰이 정상적으로 처리되지 않았을 수 있습니다.'
                }, status=status.HTTP_202_ACCEPTED
            )

        try:
            # 리프레시 토큰을 문자열에서 리프레시 토큰 객체로 형변환
            token = RefreshToken(refresh_token)
            # 리프레시 토큰을 블랙리스트에 등록하여 재사용 차단
            token.blacklist()

            # 캐시 데이터에서 리프레시 토큰 삭제
            cache.delete(f'{access_token}')

            return Response(
                {
                    'message': '로그아웃이 완료되었습니다.'
                }, status=status.HTTP_200_OK
            )
        # 리프레시 토큰 처리 중 발생할 수 있는 예외를 처리
        except (InvalidToken, TokenError) as error:
            return Response(
                {
                    'message': f'로그아웃이 완료되었습니다. 그러나 토큰 처리 중 에러가 발생했습니다. {error}'
                }, status=status.HTTP_202_ACCEPTED
            )
