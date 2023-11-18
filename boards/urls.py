from django.urls import path

from .views import ColumnCreateView


urlpatterns = [
    path('column/create/', ColumnCreateView.as_view(), name='column_create'),
]
