from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse

from .models import User


# 회원가입 관련 테스트
class UserRegisterTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # /api/v1/users/register/
        self.url = reverse('user_register')

        # 기본적으로 회원가입에 사용할 데이터
        self.user_data = {
            'username': 'test',
            'password': 'qwerty123!@#'
        }

    def test_default(self):
        response = self.client.post(self.url, self.user_data)

        # 정상적으로 회원가입에 성공하면 상태 코드 201을 반환하므로
        # 만약 상태 코드가 201이 아니라면 의도한대로 작동하지 않는 것
        if response.status_code != 201:
            print(response.data)

        # API 호출에 대한 응답으로 받은 상태 코드가 201인지 아닌지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
