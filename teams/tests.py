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
            'username': 'normaluser1',
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
            'username': 'normaluser1',
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
            'name': '첫번째팀'
        }

        # 팀 생성 API에 요청 보내기
        response = self.client.post(self.url, request_data)

        # 시리얼라이저 유효성 검사 통과 못함
        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamInviteTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/teams/invite/
        self.url = reverse('team_invite')

    # 정상적인 초대
    def test_default(self):
        # 기존 DB의 사용자 중 팀장인 사용자로 로그인 시도
        login_data = {
            'username': 'teamleader1',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 정상적으로 구성된 데이터
        request_data = {
            'target': 'normaluser4',
            'team': '첫번째팀',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 200:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 초대 상대가 입력되지 않았을 경우
    def test_no_invite_target(self):
        # 기존 DB의 사용자 중 팀장인 사용자로 로그인 시도
        login_data = {
            'username': 'teamleader1',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        #  타겟 사용자 미입력
        request_data = {
            'team': '첫번째팀',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 404:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 초대 상대가 입력되지 않았을 경우
    def test_no_team(self):
        # 기존 DB의 사용자 중 팀장인 사용자로 로그인 시도
        login_data = {
            'username': 'teamleader1',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        #  팀명 미입력
        request_data = {
            'target': 'normaluser4',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 404:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 초대 상대가 이미 다른 초대를 받고 있었을 경우
    def test_duplicated_invite(self):
        # 기존 DB의 사용자 중 팀장인 사용자로 로그인 시도
        login_data = {
            'username': 'teamleader1',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 이미 초대된 사용자를 초대
        request_data = {
            'target': 'normaluser5',
            'team': '첫번째팀',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 423:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_423_LOCKED)

    # 로그인하지 않은 사용자가 초대를 시도했을 경우
    def test_not_authenticated(self):
        # 정상적으로 구성된 데이터
        request_data = {
            'target': 'normaluser4',
            'team': '첫번째 팀',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 401:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 팀장이 아닌 사용자가 초대를 시도했을 경우
    def test_no_permission(self):
        # 기존 DB의 사용자 중 팀장이 아닌 사용자로 로그인 시도
        login_data = {
            'username': 'normaluser1',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 정상적으로 구성된 데이터
        request_data = {
            'target': 'normaluser4',
            'team': '두번째팀',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 403:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 팀장인 사용자에게 초대를 시도했을 경우
    def test_invite_leader(self):
        # 기존 DB의 사용자 중 팀장 사용자로 로그인 시도
        login_data = {
            'username': 'teamleader1',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 초대 상대가 팀장
        request_data = {
            'target': 'teamleader2',
            'team': '첫번째팀',
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 423:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_423_LOCKED)
