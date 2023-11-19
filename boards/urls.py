from django.urls import path

from .views import (
    BoardListView,
    ColumnCreateView,
    ColumnUpdateView,
    ColumnUpdateSequenceView,
    ColumnDeleteView,
    TicketCreateView,
    TicketUpdateView,
    TicketUpdateSequenceView,
)


urlpatterns = [
    path('board/list/', BoardListView.as_view(), name='board_list'),
    path('column/create/', ColumnCreateView.as_view(), name='column_create'),
    path('column/update/', ColumnUpdateView.as_view(), name='column_update'),
    path(
        'column/update/sequence/',
        ColumnUpdateSequenceView.as_view(),
        name='column_sequence_update'
    ),
    path('column/delete/', ColumnDeleteView.as_view(), name='column_delete'),
    path('ticket/create/', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/update/', TicketUpdateView.as_view(), name='ticket_update'),
    path(
        'ticket/update/sequence/',
        TicketUpdateSequenceView.as_view(),
        name='ticket_sequence_update'
    ),
]
