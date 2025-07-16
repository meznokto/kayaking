from django.urls import path

from .views import TripAPI

urlpatterns = [
    path('', TripAPI.as_view(), name='trip_api'),
]