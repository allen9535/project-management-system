from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse


# 회원가입 관련 테스트
class UserRegisterTestCase(APITestCase):
    # 테스트 DB 생성시 사용할 데이터
    # 기존 DB를 덤프해서 생성
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/users/register/
        self.url = reverse('user_register')

    # 정상적인 회원가입 케이스
    def test_default(self):
        user_data = {
            'username': 'testusername',
            'password': 'qwerty123!@#'
        }

        # 해당하는 URL에 POST 요청을 보내고 응답을 받아옴
        response = self.client.post(self.url, user_data)

        # 정상적으로 회원가입에 성공하면 상태 코드 201을 반환하므로
        # 만약 상태 코드가 201이 아니라면 의도한대로 작동하지 않는 것
        # 의도하지 않은 동작이 발생하면 관련 내용을 콘솔창에 출력
        if response.status_code != 201:
            print(response.data)

        # API 호출에 대한 응답으로 받은 상태 코드가 201인지 아닌지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 계정명을 입력하지 않은 케이스
    def test_no_username(self):
        # 회원가입에 사용할 계정명을 입력하지 않음
        user_data = {
            'password': 'qwerty123!@#'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 비밀번호를 입력하지 않은 케이스
    def test_no_password(self):
        # 회원가입에 사용할 비밀번호를 입력하지 않음
        user_data = {
            'username': 'testusername'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 계정명과 비밀번호를 모두 입력하지 않은 케이스
    def test_no_data(self):
        user_data = {}

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 계정명에 유효하지 않은 값을 입력하는 케이스(5자 미만)
    def test_invalid_username_lt_5(self):
        # 계정명에 5자 미만의 값을 입력
        user_data = {
            'username': 'abcd',
            'password': 'qwerty123!@#'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 계정명에 유효하지 않은 값을 입력하는 케이스(20자 초과)
    def test_invalid_username_gt_20(self):
        # 계정명에 20자 초과의 값을 입력
        user_data = {
            'username': 'abcdefghijklmnopqrstu',
            'password': 'qwerty123!@#'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 계정명에 유효하지 않은 값을 입력하는 케이스(이미 존재하는 계정명)
    def test_invalid_username_already_exists(self):
        # 이미 존재하는 계정명을 입력
        user_data = {
            'username': 'testuser',
            'password': 'qwerty123!@#'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 비밀번호에 유효하지 않은 값을 입력하는 케이스(5자 미만)
    def test_invalid_password_lt_5(self):
        # 비밀번호에 5자 미만의 값을 입력
        user_data = {
            'username': 'abcde',
            'password': 'qwer'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 비밀번호에 유효하지 않은 값을 입력하는 케이스(20자 초과)
    def test_invalid_password_gt_20(self):
        # 비밀번호에 20자 미만의 값을 입력
        user_data = {
            'username': 'abcde',
            'password': 'qwerty1234567890qwert'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 사용자 모델에 있는 필드이지만,
    # 회원가입 시나리오에서 입력받지 않는 값을 입력한 경우
    def test_valid_another_data(self):
        # message 필드는 사용자 모델에 있기는 하지만,
        # serializer 단에서 받아들이지 않음
        user_data = {
            'username': 'abcde',
            'password': 'qwerty123!@#',
            'message': 'test message'
        }

        response = self.client.post(self.url, user_data)

        if response.status_code != 201:
            print(response.data)

        # 하지만 에러는 발생하지 않음
        # 계정명과 비밀번호를 입력했다면 계정은 생성됨
        # 별도의 값은 입력되지 않음
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    # 테스트 DB 생성시 사용할 데이터
    # 기존 DB를 덤프해서 생성
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/users/login/
        self.url = reverse('login')

    # 정상적인 로그인 케이스
    def test_default(self):
        # DB 데이터에 있는 계정을 입력
        login_data = {
            'username': 'testuser',
            'password': 'qwerty123!@#'
        }

        response = self.client.post(self.url, login_data)

        if response.status_code != 200:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 계정명을 입력하지 않는 경우
    def test_no_username(self):
        login_data = {
            'password': 'qwerty123!@#'
        }

        response = self.client.post(self.url, login_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 비밀번호를 입력하지 않는 경우
    def test_no_username(self):
        login_data = {
            'username': 'testuser'
        }

        response = self.client.post(self.url, login_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 계정명과 비밀번호를 모두 입력하지 않는 경우
    def test_no_data(self):
        login_data = {}

        response = self.client.post(self.url, login_data)

        if response.status_code != 400:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 잘못된 계정명을 입력한 경우
    def test_invalid_username(self):
        login_data = {
            'username': 'invalidtestuser',
            'password': 'qwerty123!@3'
        }

        response = self.client.post(self.url, login_data)

        if response.status_code != 404:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 잘못된 비밀번호를 입력한 경우
    def test_invalid_password(self):
        login_data = {
            'username': 'testuser',
            'password': 'invalidpassword'
        }

        response = self.client.post(self.url, login_data)

        if response.status_code != 404:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# 로그아웃 기능은 대개 토큰을 다루는 기능이므로 테스트가 어려움
# 따라서 정상적인 로그아웃 케이스와 로그인되지 않은 상태에서의 로그아웃 케이스만 다룸
class LogoutTestCase(APITestCase):
    # 테스트 DB 생성시 사용할 데이터
    # 기존 DB를 덤프해서 생성
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/users/logout/
        self.url = reverse('logout')

    # 정상적인 로그아웃 케이스
    # 정상적이지 않은 로그아웃 케이스도 테스트해야 하므로
    # 테스트 내부에서 로그인 진행
    def test_default(self):
        # 로그인 데이터 생성
        login_data = {
            'username': 'testuser',
            'password': 'qwerty123!@#'
        }

        # 로그인 후 발급된 액세스 토큰 담기
        access_token = self.client.post(
            reverse('login'),
            login_data
        ).data.get('access')

        # APIClient 객체에 인증 진행
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        response = self.client.post(self.url)

        if response.status_code != 200:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 로그인하지 않은 상태에서의 로그아웃
    def test_logout_without_login(self):
        response = self.client.post(self.url)

        # 인증되지 않은 사용자이므로 상태코드 401이 반환됨
        if response.status_code != 401:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
