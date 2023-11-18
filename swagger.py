from drf_yasg import openapi


USER_REGISTER_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='계정명'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
    }
)

LOGIN_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='계정명'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
    }
)

TEAM_CREATE_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='팀명')
    }
)

TEAM_INVITE_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'target': openapi.Schema(type=openapi.TYPE_STRING, description='초대할 사용자명'),
        'team': openapi.Schema(type=openapi.TYPE_STRING, description='초대하는 팀명')
    }
)

COLUMN_CREATE_PARAMETER = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'team': openapi.Schema(type=openapi.TYPE_STRING, description='팀명'),
        'title': openapi.Schema(type=openapi.TYPE_STRING, description='컬럼 제목')
    }
)
