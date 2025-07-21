from django.urls import path

from .views import KayakUsersAPI

urlpatterns = [
    path('', KayakUsersAPI.as_view(), name='users_api'),
]