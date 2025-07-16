from django.urls import path

from .views import WaterAPI

urlpatterns = [
    path('', WaterAPI.as_view(), name='water_api'),
]