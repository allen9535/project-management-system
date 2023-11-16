from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse


# 팀 생성 테스트
class TeamCreateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/teams/create/
        self.url = reverse('team_create')

    # 정상적인 팀 생성 케이스
    def test_default(self):
        # 기존 DB의 사용자 중 아직 팀을 생성하지 않은 사용자로 로그인 시도
        login_data = {
            'username': 'testuser2',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 팀 생성에 필요한 데이터 생성
        request_data = {
            'name': '팀명'
        }

        # 팀 생성 API에 요청 보내기
        response = self.client.post(self.url, request_data)

        if response.status_code != 201:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 이미 존재하는 이름의 팀명 사용하는 케이스
    def test_duplicated_team_name(self):
        # 기존 DB의 사용자 중 아직 팀을 생성하지 않은 사용자로 로그인 시도
        login_data = {
            'username': 'testuser2',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 이미 존재하는 팀명 사용
        request_data = {
            'name': '첫번째 팀'
        }

        # 팀 생성 API에 요청 보내기
        response = self.client.post(self.url, request_data)

        # 시리얼라이저 유효성 검사 통과 못함
        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 이미 한 번 팀을 만들어 팀장인 사용자가
    # 다시 팀 생성을 시도하는 케이스
    def test_create_another_team(self):
        # 기존 DB의 사용자 중 이미 팀을 생성한 사용자로 로그인 시도
        login_data = {
            'username': 'testuser',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 새 팀명 사용
        request_data = {
            'name': '첫번째 팀'
        }

        # 팀 생성 API에 요청 보내기
        response = self.client.post(self.url, request_data)

        # 권한 오류가 발생하기 때문에 상태코드는 403이 나옴
        if response.status_code != 403:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
