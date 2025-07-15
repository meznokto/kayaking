from django.urls import path

from .views import LaunchesAPI

urlpatterns = [
    path('', LaunchesAPI.as_view(), name='launches_api'),
]