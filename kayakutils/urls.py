from django.urls import path

from .views import CityAPI

urlpatterns = [
    path('cities/', CityAPI.as_view(), name='cities_api'),
]
