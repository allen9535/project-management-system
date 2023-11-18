from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse


# 컬럼 생성 테스트
class ColumnCreateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/create/
        self.url = reverse('column_create')

    # 정상적인 컬럼 생성 케이스
    def test_default(self):
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

        # 컬럼 생성에 필요한 데이터 생성
        request_data = {
            'team': '첫번째팀',  # 기존 DB의 해당 사용자의 팀 입력
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 201:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 컬럼 제목을 입력하지 않고 컬럼 생성을 시도하는 케이스
    def test_no_title(self):
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

        # 컬럼 생성에 필요한 데이터 생성
        # 컬럼 제목이 없음
        request_data = {
            'team': '첫번째팀',  # 기존 DB의 해당 사용자의 팀 입력
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 팀명을 입력하지 않고 컬럼 생성을 시도하는 케이스
    def test_no_team(self):
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

        # 컬럼 생성에 필요한 데이터 생성
        # 팀명이 없음
        request_data = {
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 팀장이 본인의 팀이 아닌 다른 팀에 컬럼 생성을 시도하는 케이스
    def test_other_team(self):
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

        # 컬럼 생성에 필요한 데이터 생성
        request_data = {
            'team': '두번째팀',  # 기존 DB의 다른 사용자의 팀 입력
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        # 권한 문제이기 때문에 상태코드는 403이 나옴
        if response.status_code != 403:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 팀장이 아닌 사용자가 컬럼 생성을 시도하는 케이스
    def test_not_leader(self):
        # 기존 DB의 사용자 중 팀장 사용자로 로그인 시도
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

        # 컬럼 생성에 필요한 데이터 생성
        request_data = {
            'team': '첫번째팀',  # 기존 DB의 본인 팀 입력
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        # 권한 문제이기 때문에 상태코드는 403이 나옴
        if response.status_code != 403:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 로그인하지 않은 사용자가 임의의 팀에 컬럼 생성을 시도하는 케이스
    def test_not_authorized(self):
        # 컬럼 생성에 필요한 데이터 생성
        request_data = {
            'team': '첫번째팀',  # 기존 DB의 다른 사용자의 팀 입력
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        # 인증 문제이기 때문에 상태코드는 401이 나옴
        if response.status_code != 401:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# 보드 목록 테스트
class BoardListTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/board/list/
        self.url = reverse('board_list')

    # 팀장이 보드를 확인하는 케이스
    def test_leader_reads(self):
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

        response = self.client.get(self.url)

        if response.status_code != 200:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 팀원이 보드를 확인하는 케이스
    def test_teammate_reads(self):
        # 기존 DB의 사용자 중 팀원 사용자로 로그인 시도
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

        response = self.client.get(self.url)

        if response.status_code != 200:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 팀에 소속되지 않은 사용자가 보드를 확인하는 케이스
    def test_outsider_reads(self):
        # 기존 DB의 사용자 중 팀에 소속되지 않은 사용자로 로그인 시도
        login_data = {
            'username': 'normaluser4',
            'password': 'qwerty123!@#'
        }

        # 해당 데이터로 로그인 후 액세스 토큰 획득
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(self.url)

        # 권한 문제이기 때문에 상태코드는 403이 나옴
        if response.status_code != 403:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 인증되지 않은 사용자가 보드를 확인하는 케이스
    def test_outsider_reads(self):
        response = self.client.get(self.url)

        # 인증 문제이기 때문에 상태코드는 401이 나옴
        if response.status_code != 401:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
