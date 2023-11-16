from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterSerializer


# /api/v1/users/register/
class UserRegisterView(APIView):
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
