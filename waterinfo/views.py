from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.exceptions import APIException # type: ignore
from rest_framework import status # type: ignore
from django.shortcuts import get_object_or_404

from .models import Water
from .serializers import WaterSerializer

class WaterAPI(APIView):
    queryset = Water.objects.all().order_by('-date_updated')
    serializer_class = WaterSerializer

    def get(self, request):
        # if a water parameter was provided, show only results for that water
        # this allows for more efficient queries by only returning necessary fields
        # e.g., ?water=123
        # if no water is specified, return all launches
        if 'water' in request.GET:
            waters = Water.objects.filter(pk=request.GET['water'])
            if not waters.exists():
                # if the launch does not exist, raise a 404 error
                raise APIException('No such water found.')
        else:
            waters = self.queryset.all()
        
        if 'country' in request.GET:
            country = request.GET['country']
            waters = self.queryset.filter(country__id=country)
            if not waters.exists():
                raise APIException('No waters found.')
            
        if 'state' in request.GET:
            state = request.GET['state']
            waters = self.queryset.filter(state__id=state)
            if not waters.exists():
                raise APIException('No waters found.')
            
        if 'county' in request.GET:
            county = request.GET['county']
            waters = self.queryset.filter(county__id=county)
            if not waters.exists():
                raise APIException('No waters found.')
            
        if 'city' in request.GET:
            city = request.GET['city']
            waters = self.queryset.filter(city__id=city)
            if not waters.exists():
                raise APIException('No waters found.')

        if 'fields' in request.GET:
            if request.GET['fields'] == 'all':
                fields = None
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
                fields = ('id', 'name', 'city', 'state', 'country')
        serializer = WaterSerializer(waters, many=True, fields=fields)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            water = serializer.save()
            return Response(WaterSerializer(water).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        water = get_object_or_404(Water, pk=pk)
        serializer = self.serializer_class(water, data=request.data)
        if serializer.is_valid():
            updated_water = serializer.save()
            return Response(WaterSerializer(updated_water).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        water = get_object_or_404(Water, pk=pk)
        water.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  