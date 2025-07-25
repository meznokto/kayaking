from django.urls import path

from .views import CityAPI, CountryAPI, StateAPI, CountyAPI

urlpatterns = [
    path('countries/', CountryAPI.as_view(), name='countries_api'),
    path('states/', StateAPI.as_view(), name='states_api'),
    path('counties/', CountyAPI.as_view(), name='counties_api' ),
    path('cities/', CityAPI.as_view(), name='cities_api'),
]
