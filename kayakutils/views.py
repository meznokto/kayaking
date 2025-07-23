from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.exceptions import APIException # type: ignore
from rest_framework import status # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.shortcuts import get_object_or_404

from .models import Country, State, City, County
from launchinfo.serializers import CitySerializer, StateSerializer, CountySerializer, CountrySerializer

class StateNotGivenException(APIException):
    status_code = 404
    default_detail = 'No state provided.'
    default_code = 'no_state_given'

class CitiesNotFoundException(APIException):
    status_code = 404
    default_detail = 'No cities found.'
    default_code = 'no_cities_found'

class CityAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    #queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer

    def get(self, request):
        if 'state' in request.GET:
            cities = City.objects.filter(state=request.GET['state'])
            if not cities.exists():
                raise CitiesNotFoundException()
        else:
            raise StateNotGivenException()

        serializer = CitySerializer(cities, many=True, fields=('id', 'name'))
        return Response(serializer.data)

