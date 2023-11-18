from django.urls import path

from .views import BoardListView, ColumnCreateView


urlpatterns = [
    path('board/list/', BoardListView.as_view(), name='board_list'),
    path('column/create/', ColumnCreateView.as_view(), name='column_create'),
]
