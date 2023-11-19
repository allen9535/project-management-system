from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse


# 컬럼 생성 테스트
class ColumnCreateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/column/create/
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
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.data
        )

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
        request_data = {}

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

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
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        # 권한 문제이기 때문에 상태코드는 403이 나옴
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 로그인하지 않은 사용자가 임의의 팀에 컬럼 생성을 시도하는 케이스
    def test_not_authorized(self):
        # 컬럼 생성에 필요한 데이터 생성
        request_data = {
            'title': 'Backlog'
        }

        response = self.client.post(self.url, request_data)

        # 인증 문제이기 때문에 상태코드는 401이 나옴
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


# 컬럼 수정 테스트
class ColumnUpdateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/column/update/
        self.url = reverse('column_update')

    # 정상적인 컬럼 수정 케이스
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

        # 컬럼 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'title': 'update'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 컬럼 id 없이 수정을 시도하는 케이스
    def test_no_column_id(self):
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

        # 수정할 컬럼 제목 데이터만 제공
        request_data = {
            'title': 'update'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 수정할 컬럼 제목 데이터 없이 수정을 시도하는 케이스
    def test_no_update_data(self):
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

        # 컬럼 id 값만 제공
        request_data = {
            'column': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 수정할 데이터 없이 수정을 시도하는 케이스
    def test_no_data(self):
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

        # 데이터 없음
        request_data = {}

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 유효하지 않은 값으로 수정을 시도하는 케이스
    def test_invalid_id(self):
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

        # 컬럼 id 값이 유효하지 않음
        request_data = {
            'column': 'INVALID',
            'title': 'update'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 존재하지 않는 컬럼 id를 입력하는 케이스
    def test_column_out_of_range(self):
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

        # 존재하지 않는 컬럼 id를 입력함
        request_data = {
            'column': 100,
            'title': 'update'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 컬럼 순서 변경을 시도하는 케이스
    def test_sequence_update(self):
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

        # 존재하지 않는 컬럼 id를 입력함
        request_data = {
            'column': 1,
            'title': 'update',
            'sequence': 10
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 팀에 소속되지 않은 사용자가 변경을 시도하는 케이스
    def test_not_teammate(self):
        # 기존 DB의 사용자 중 팀장 사용자로 로그인 시도
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

        # 정상적인 데이터
        request_data = {
            'column': 1,
            'title': 'update'
        }

        response = self.client.put(self.url, request_data)

        # 팀 구성원 전체에 권한이 부여되므로, 팀에 소속되지 않으면 사용 불가
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 인증되지 않은 사용자가 변경을 시도하는 케이스
    def test_not_authorized(self):
        # 정상적인 데이터
        request_data = {
            'column': 1,
            'title': 'update'
        }

        response = self.client.put(self.url, request_data)

        # 인증된 사용자에게 권한을 부여하므로, 인증되지 않으면 사용 불가
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


# 컬럼 순서 수정 테스트
class ColumnSequenceUpdateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/column/update/sequence/
        self.url = reverse('column_sequence_update')

    # 컬럼 순서가 기존보다 뒤로 가는 케이스
    def test_sequence_right(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'sequence': 3
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 컬럼 순서가 기존보다 앞으로 가는 케이스
    def test_sequence_left(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 3,
            'sequence': 2
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 원래 값을 변경 값으로 받은 케이스
    def test_sequence_stand(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 2,
            'sequence': 2
        }

        response = self.client.put(self.url, request_data)

        # 값이 변할 건 없으므로 상태코드 200
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 유효하지 않은 컬럼 id 값을 받은 케이스
    def test_invalid_column(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 'INVALID',
            'sequence': 2
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 유효하지 않은 변경 값을 받은 케이스
    def test_invalid_sequence(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'sequence': 'INVALID'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 0 이하의 순서값을 받은 케이스
    def test_sequence_under_0(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'sequence': 0
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 현재 보드 내 컬럼 갯수보다 큰 순서값을 받은 케이스
    def test_sequence_over_len(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'sequence': 100
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 입력값이 없는 케이스
    def test_sequence_no_data(self):
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

        # 데이터가 없음
        request_data = {}

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 권한이 없는(소속된 팀이 없는) 케이스
    def test_no_permission(self):
        # 기존 DB의 사용자 중 팀이 없는 사용자로 로그인 시도
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'sequence': 3
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 인증이 없는(로그인이 되지 않은) 케이스
    def test_no_authorize(self):
        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'column': 1,
            'sequence': 3
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


# 컬럼 삭제 테스트
class ColumnDeleteTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/column/delete/
        self.url = reverse('column_delete')

    # 정상적인 컬럼 삭제 케이스
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

        # 컬럼 삭제에 필요한 데이터 생성
        request_data = {
            'column': 1,
        }

        response = self.client.delete(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 컬럼 id 없이 삭제를 시도하는 케이스
    def test_no_column_id(self):
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

        # 데이터가 없음
        request_data = {}

        response = self.client.delete(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 유효하지 않은 값으로 삭제를 시도하는 케이스
    def test_invalid_id(self):
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

        # 컬럼 id 값이 유효하지 않음
        request_data = {
            'column': 'INVALID'
        }

        response = self.client.delete(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 존재하지 않는 컬럼 id를 입력하는 케이스
    def test_column_out_of_range(self):
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

        # 존재하지 않는 컬럼 id를 입력함
        request_data = {
            'column': 100
        }

        response = self.client.delete(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 팀장이 아닌 사용자가 삭제를 시도하는 케이스
    def test_not_leader(self):
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

        # 정상적인 데이터
        request_data = {
            'column': 1
        }

        response = self.client.delete(self.url, request_data)

        # 컬럼은 팀장만 삭제 가능
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.data
        )

    # 팀에 소속되지 않은 사용자가 삭제를 시도하는 케이스
    def test_not_teammate(self):
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

        # 정상적인 데이터
        request_data = {
            'column': 1
        }

        response = self.client.delete(self.url, request_data)

        # 해당 팀의 팀장에만 컬럼 삭제 권한이 주어짐
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 인증되지 않은 사용자가 변경을 시도하는 케이스
    def test_not_teammate(self):
        # 정상적인 데이터
        request_data = {
            'column': 1
        }

        response = self.client.delete(self.url, request_data)

        # 인증된 사용자에게 권한을 부여하므로, 인증되지 않으면 사용 불가
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


# 티켓 생성 테스트
class TicketCreateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/ticket/create/
        self.url = reverse('ticket_create')

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
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.data
        )

    # 담당자는 입력하지 않지만 정상적인 컬럼 생성 케이스
    def test_default_no_charge(self):
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
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.data
        )

    # 제목을 입력하지 않고 생성을 시도하는 케이스
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

        # 제목이 없는 데이터 생성
        request_data = {
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 태그를 입력하지 않고 생성을 시도하는 케이스
    def test_no_tag(self):
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

        # 태그가 없는 데이터 생성
        request_data = {
            'title': '테스트',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 업무량을 입력하지 않고 생성을 시도하는 케이스
    def test_no_volume(self):
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

        # 업무량이 없는 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 마감일을 입력하지 않고 생성을 시도하는 케이스
    def test_no_ended_at(self):
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

        # 마감일이 없는 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 컬럼 id를 입력하지 않고 생성을 시도하는 케이스
    def test_no_column(self):
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

        # 컬럼 id가 없는 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 유효하지 않은 컬럼 id를 입력해 생성을 시도하는 케이스
    def test_invalid_column(self):
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

        # 컬럼 id가 유효하지 않은 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 'INVALID',
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 없는 컬럼 id를 입력해 생성을 시도하는 케이스
    def test_column_id(self):
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

        # 컬럼 id가 유효하지 않은 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 5,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 유효하지 않은 담당자를 입력해 생성을 시도하는 케이스
    def test_invalid_charge(self):
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

        # 담당자 유효하지 않은 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'INVALID'
        }

        response = self.client.post(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 팀에 소속되지 않은 사용자가 컬럼 생성을 시도하는 케이스
    def test_not_teammate(self):
        # 기존 DB의 사용자 중 팀이 없는 사용자로 로그인 시도
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

        # 티켓 생성에 필요한 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        # 권한 문제이기 때문에 상태코드는 403이 나옴
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 로그인하지 않은 사용자가 티켓 생성을 시도하는 케이스
    def test_not_authorized(self):
        # 티켓 생성에 필요한 데이터 생성
        request_data = {
            'title': '테스트',
            'tag': 'BE',
            'volume': 4.0,
            'ended_at': '2023-11-19',
            'column': 1,
            'charge': 'normaluser1'
        }

        response = self.client.post(self.url, request_data)

        # 인증 문제이기 때문에 상태코드는 401이 나옴
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


# 티켓 수정 테스트
class TicketUpdateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/ticket/update/
        self.url = reverse('ticket_update')

    # 정상적인 티켓 수정 케이스
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

        # 티켓 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': '2023-11-20',
            'charge': 'normaluser1'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 팀원이 시도하는 정상적인 티켓 수정 케이스
    def test_default_teammate(self):
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

        # 티켓 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': '2023-11-20',
            'charge': 'teamleader1'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 티켓 id 없이 수정을 시도하는 케이스
    def test_no_ticket_id(self):
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

        # 티켓 id 없음
        request_data = {
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': '2023-11-20',
            'charge': 'normaluser1'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 잘못된 티켓 id로 수정을 시도하는 케이스
    def test_invalid_ticket_id(self):
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

        # 유효하지 않은 티켓 id
        request_data = {
            'ticket': 'INVALID',
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': '2023-11-20',
            'charge': 'teamleader1'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 없는 티켓 id로 수정을 시도하는 케이스
    def test_ticket_id_over(self):
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

        # 유효하지 않은 티켓 id
        request_data = {
            'ticket': 3,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': '2023-11-20',
            'charge': 'teamleader1'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 담당자 데이터 없이 수정을 시도하는 케이스
    def test_no_charge(self):
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

        # 담당자 데이터 없음
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': '2023-11-20'
        }

        response = self.client.put(self.url, request_data)

        # 정상적으로 값이 수정되어야 함
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 유효하지 않은 태그로 수정을 시도하는 케이스
    def test_invalid_tag(self):
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

        # 유효하지 않은 태그값
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'INVALID',
            'volume': 4,
            'ended_at': '2023-11-20'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 수정할 데이터 없이 수정을 시도하는 케이스
    def test_no_data(self):
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

        # 데이터 없음
        request_data = {}

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 티켓 순서 변경을 시도하는 케이스
    def test_sequence_update(self):
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

        # 티켓 순서를 입력함
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': 2023-11-20,
            'charge': 'normaluser1',
            'sequence': 10
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 팀에 소속되지 않은 사용자가 변경을 시도하는 케이스
    def test_not_teammate(self):
        # 기존 DB의 사용자 중 팀에 소속되지 않은 사용자로 로그인
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

        # 정상적인 데이터
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': 2023-11-20,
            'charge': 'normaluser1'
        }

        response = self.client.put(self.url, request_data)

        # 팀 구성원 전체에 권한이 부여되므로, 팀에 소속되지 않으면 사용 불가
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 인증되지 않은 사용자가 변경을 시도하는 케이스
    def test_not_authorized(self):
        # 정상적인 데이터
        request_data = {
            'ticket': 1,
            'title': 'update',
            'tag': 'Doc',
            'volume': 4,
            'ended_at': 2023-11-20,
            'charge': 'normaluser1'
        }

        response = self.client.put(self.url, request_data)

        # 인증된 사용자에게 권한을 부여하므로, 인증되지 않으면 사용 불가
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


# 티켓 순서 수정 테스트
class TicketSequenceUpdateTestCase(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        # APIClient 객체 생성
        self.client = APIClient()

        # /api/v1/boards/ticket/update/sequence/
        self.url = reverse('ticket_sequence_update')

    # 티켓이 현재 컬럼에서 뒷순서로 가는 케이스
    def test_sequence_down(self):
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

        # 현재 컬럼에서 티켓 순서만 뒤로가는 데이터 생성
        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 2
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 티켓이 현재 컬럼에서 앞순서로 가는 케이스
    def test_sequence_up(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 2,
            'column_sequence': 1,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 티켓이 옆 컬럼으로 가는 케이스
    def test_sequence_left_right(self):
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

        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'column_sequence': 2,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 원래 값을 변경 값으로 받은 케이스
    def test_sequence_stand(self):
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

        # 순서 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        # 값이 변할 건 없으므로 상태코드 200
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    # 컬럼 순서를 입력하지 않은 케이스
    def test_no_column(self):
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

        # 순서 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'ticket_sequence': 2
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 티켓 순서를 입력하지 않은 케이스
    def test_no_ticket(self):
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

        # 순서 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'column_sequence': 2
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 유효하지 않은 티켓 id 값을 받은 케이스
    def test_invalid_ticket(self):
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

        # 티켓 id가 유효하지 않은 데이터 생성
        request_data = {
            'ticket': 'INVALID',
            'column_sequence': 1,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 없는 티켓 id 값을 받은 케이스
    def test_ticket_over(self):
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

        # 티켓 id가 기존 값을 넘은 데이터 생성
        request_data = {
            'ticket': 100,
            'column_sequence': 1,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 유효하지 않은 컬럼 변경 값을 받은 케이스
    def test_invalid_column_sequence(self):
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

        # 컬럼 변경값이 유효하지 않은 데이터
        request_data = {
            'ticket': 1,
            'column_sequence': 'INVALID',
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 유효하지 않은 티켓 변경 값을 받은 케이스
    def test_invalid_ticket_sequence(self):
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

        # 티켓 변경값이 유효하지 않은 데이터
        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 'INVALID'
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 0 이하의 컬럼 변경값을 받은 케이스
    def test_column_sequence_under_0(self):
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

        # 컬럼 변경값이 0이하인 데이터
        request_data = {
            'ticket': 1,
            'column_sequence': 0,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 0 이하의 티켓 변경값을 받은 케이스
    def test_ticket_sequence_under_0(self):
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

        # 티켓 변경값이 0이하인 데이터
        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 0
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 현재 보드 내 컬럼 갯수보다 큰 컬럼 변경값을 받은 케이스
    def test_column_len_over(self):
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

        # 전체 컬럼 갯수보다 큰 컬럼 변경값 데이터
        request_data = {
            'ticket': 1,
            'column_sequence': 100,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 현재 컬럼 내 티켓 갯수보다 큰 티켓 변경값을 받은 케이스
    def test_ticket_len_over(self):
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

        # 전체 컬럼 갯수보다 큰 컬럼 변경값 데이터
        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 100
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

    # 입력값이 없는 케이스
    def test_no_data(self):
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

        # 데이터가 없음
        request_data = {}

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.data
        )

    # 권한이 없는(소속된 팀이 없는) 케이스
    def test_no_permission(self):
        # 기존 DB의 사용자 중 팀이 없는 사용자로 로그인 시도
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

        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 인증이 없는(로그인이 되지 않은) 케이스
    def test_no_authorize(self):
        # 컬럼 순서 수정에 필요한 데이터 생성
        request_data = {
            'ticket': 1,
            'column_sequence': 1,
            'ticket_sequence': 1
        }

        response = self.client.put(self.url, request_data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )


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

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

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

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

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
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.data
        )

    # 인증되지 않은 사용자가 보드를 확인하는 케이스
    def test_outsider_reads(self):
        response = self.client.get(self.url)

        # 인증 문제이기 때문에 상태코드는 401이 나옴
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )
