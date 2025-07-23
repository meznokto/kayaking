from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.exceptions import APIException # type: ignore
from rest_framework import status # type: ignore
from django.shortcuts import get_object_or_404

from .models import Launch
from .serializers import LaunchSerializer

class LaunchesAPI(APIView):
    queryset = Launch.objects.all().order_by('-date_updated')
    serializer_class = LaunchSerializer

    def get(self, request):
        # if a launch parameter was provided, show only results for that launch
        # this allows for more efficient queries by only returning necessary fields
        # e.g., ?launch=123
        # if no launch is specified, return all launches
        if 'launch' in request.GET:
            launches = Launch.objects.filter(pk=request.GET['launch'])
            if not launches.exists():
                # if the launch does not exist, raise a 404 error
                raise APIException('No such launch found.')
        else:
            launches = self.queryset.all()

        # if a waterid was provided, show only launches on that body of water
        if 'waterid' in request.GET:
            waterid = request.GET['waterid']
            launches = self.queryset.filter(body_of_water__id=waterid)
            if not launches.exists():
                # if no launches are found for the given water body, raise a 404 error
                raise APIException('No launches found.')
        
        if 'country' in request.GET:
            country = request.GET['country']
            launches = self.queryset.filter(country__id=country)
            if not launches.exists():
                raise APIException('No launches found.')
        elif 'state' in request.GET:
            state = request.GET['state']
            launches = self.queryset.filter(state__id=state)
            if not launches.exists():
                raise APIException('No launches found.')
        elif 'county' in request.GET:
            county = request.GET['county']
            launches = self.queryset.filter(county__id=county)
            if not launches.exists():
                raise APIException('No launches found.')
        elif 'city' in request.GET:
            city = request.GET['city']
            launches = self.queryset.filter(city__id=city)
            if not launches.exists():
                raise APIException('No launches found.')

        # if a field parameter was provided, filter the fields
        # this allows for more efficient queries by only returning necessary fields
        # e.g., ?field=name&field=latitude&field=longitude
        # can also get all fields with fields=all or field=all
        if 'fields' in request.GET:
            if request.GET['fields'] == 'all':
                fields = None  # return all fields
        else:
            if 'field' in request.GET:
                if request.GET['field'] == 'all':
                    # should we check and not allow all fields if
                    # no launch is specified?
                    fields = None  # return all fields
                else:
                    # if specific fields are requested, filter them
                    fields = request.GET.getlist('field')
                    fields.append('id') # always include the ID field
            else:
                # if no fields are specified, return a default set
                # this is useful for listing launches in a compact format
                fields = ('id', 'name', 'city', 'state', 'country', 'body_of_water', 'thumbnail')
        serializer = LaunchSerializer(launches, many=True, fields=fields)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            launch = serializer.save()
            return Response(LaunchSerializer(launch).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        launch = get_object_or_404(Launch, pk=pk)
        serializer = self.serializer_class(launch, data=request.data)
        if serializer.is_valid():
            updated_launch = serializer.save()
            return Response(LaunchSerializer(updated_launch).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
