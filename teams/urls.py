from django.urls import path

from .views import TeamCreateView, TeamInviteView


urlpatterns = [
    path('create/', TeamCreateView.as_view(), name='team_create'),
    path('invite/', TeamInviteView.as_view(), name='team_invite'),
]
