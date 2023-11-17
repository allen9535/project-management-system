from django.urls import path

from .views import (
    UserRegisterView,
    LoginView,
    LogoutView,
    UserInviteDetailView,
    UserInviteAcceptView
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('invite/', UserInviteDetailView.as_view(), name='read_invite'),
    path('invite/accept/', UserInviteAcceptView.as_view(), name='accept_invite'),
]
