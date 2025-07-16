from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.exceptions import APIException # type: ignore
from rest_framework import status # type: ignore
from django.shortcuts import get_object_or_404

from .models import Trip
from .serializers import TripSerializer

class TripNotFoundException(APIException):
    status_code = 404
    default_detail = 'Trip not found.'
    default_code = 'trip_not_found'

class TripAPI(APIView):
    queryset = Trip.objects.all().order_by('-start_time')
    serializer_class = TripSerializer

    def get(self, request):
        if 'trip' in request.GET:
            trips = Trip.objects.filter(id=request.GET['trip'], is_private=False)
            if not trips.exists():
                raise TripNotFoundException()
        else:
            trips = self.queryset.all().filter(is_private=False)
            
        if 'fields' in request.GET:
            if request.GET['fields'] == 'all':
                fields = None
        else:
            if 'field' in request.GET:
                if request.GET['field'] == 'all':
                    fields = None
                else:
                    fields = request.GET.getlist('field')
                    fields.append('id')  # always include the ID field
            else:
                fields = ('id', 'body_of_water', 'start_time')  # default fields

        serializer = TripSerializer(trips, many=True, fields=fields)
        return Response(serializer.data)

    def post(self, request):
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            trip = serializer.save()
            return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        serializer = TripSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid():
            updated_trip = serializer.save()
            return Response(TripSerializer(updated_trip).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)