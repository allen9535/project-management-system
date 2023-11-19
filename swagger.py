from drf_yasg import openapi


SUCCESS_MESSAGE_200 = '성공적으로 요청을 완료했습니다.'
SUCCESS_MESSAGE_201 = '성공적으로 데이터 생성을 완료했습니다.'
SUCCESS_MESSAGE_204 = '성공적으로 요청을 완료했습니다. 그러나 반환할 값이 없습니다.'
ERROR_MESSAGE_400 = '입력값 오류, 잘못된 값이 입력되었습니다. 상세한 내용은 에러 메시지를 확인해주세요.'
ERROR_MESSAGE_401 = '인증 오류, 인증되지 않은 사용자는 이용할 수 없습니다.'
ERROR_MESSAGE_403 = '권한 오류, 권한이 없는 사용자는 이용할 수 없습니다.'
ERROR_MESSAGE_404 = '입력값 오류, 잘못된 값으로 인해 데이터를 찾을 수 없습니다.'
ERROR_MESSAGE_423 = '상태 오류, 요청이 완료될 수 없는 상태입니다.'
ERROR_MESSAGE_500 = '서버 오류, 요청을 처리하던 중 서버에 문제가 발생했습니다.'

USER_REGISTER_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='계정명'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
    },
    required=['username', 'password']
)

LOGIN_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='계정명'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
    },
    required=['username', 'password']
)

TEAM_CREATE_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='팀명')
    },
    required=['name']
)

TEAM_INVITE_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'target': openapi.Schema(type=openapi.TYPE_STRING, description='초대할 사용자명')
    },
    required=['target']
)

COLUMN_CREATE_PARAMETER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='컬럼 제목')
    },
    required=['title']
)

COLUMN_UPDATE_PARAMETER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'column': openapi.Schema(type=openapi.TYPE_INTEGER, description='컬럼 id'),
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='컬럼 제목')
    },
    required=['column']
)

COLUMN_UPDATE_SEQUENCE_PARAMETER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'column': openapi.Schema(type=openapi.TYPE_INTEGER, description='컬럼 id'),
        'sequence': openapi.Schema(type=openapi.TYPE_STRING, description='컬럼 순서')
    },
    required=['column', 'sequence']
)

COLUMN_DELETE_PARAMETER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'column': openapi.Schema(type=openapi.TYPE_INTEGER, description='컬럼 id')
    },
    required=['column']
)

TICKET_CREATE_PARAMETER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'column': openapi.Schema(type=openapi.TYPE_INTEGER, description='컬럼 id'),
        'charge': openapi.Schema(type=openapi.TYPE_STRING, description='담당자 계정명'),
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='티켓 제목'),
        'tag': openapi.Schema(type=openapi.TYPE_STRING, description='태그'),
        'volume': openapi.Schema(type=openapi.TYPE_NUMBER, description='작업량'),
        'ended_at': openapi.Schema(type=openapi.TYPE_STRING, description='마감일')
    },
    required=['column', 'title', 'tag', 'volume', 'ended_at']
)
