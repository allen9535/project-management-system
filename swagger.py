from drf_yasg import openapi


USER_REGISTER_PARAMETERS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='계정명'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='계정명')
    }
)
