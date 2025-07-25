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

class CityAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    #queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer

    def get(self, request):
        if 'state' in request.GET:
            cities = City.objects.filter(state=request.GET['state'])
            if not cities.exists():
                raise APIException('No cities found for the given state.')
        elif 'county' in request.GET:
            cities = City.objects.filter(state=request.GET['county'])
            if not cities.exists():
                raise APIException('No cities found for the given county.')
        else:
            raise APIException('No state or county provided.')

        serializer = CitySerializer(cities, many=True, fields=('id', 'name'))
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            city = serializer.save()
            return Response(CitySerializer(city).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountryAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    serializer_class = CountrySerializer

    def get(self, request):
        countries = Country.objects.all().order_by('name')
        serializer = CountrySerializer(countries, many=True, fields=('id', 'name'))
        return Response(serializer.data)
    
class StateAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    serializer_class = StateSerializer

    def get(self, request):
        if 'country' in request.GET:
            states = State.objects.filter(country=request.GET['country'])
            if not states.exists():
                raise APIException('No states found for the given country.')
        else:
            raise APIException('No country provided.')

        serializer = StateSerializer(states, many=True, fields=('id', 'name'))
        return Response(serializer.data)
    
class CountyAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only allow authenticated users

    serializer_class = CountySerializer

    def get(self, request):
        if 'state' in request.GET:
            counties = County.objects.filter(state=request.GET['state'])
            if not counties.exists():
                raise APIException('No counties found for the given state.')
        else:
            raise APIException('No state provided.')

        serializer = CountySerializer(counties, many=True, fields=('id', 'name'))
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            city = serializer.save()
            return Response(CountySerializer(city).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)