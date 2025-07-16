from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .models import Water
from .serializers import WaterSerializer

class WaterNotFoundException(APIException):
    status_code = 404
    default_detail = 'Water not found.'
    default_code = 'water_not_found'

class WaterAPI(APIView):
    queryset = Water.objects.all().order_by('-date_updated')
    serializer_class = WaterSerializer

    def get(self, request):
        if 'water' in request.GET:
            waters = Water.objects.filter(pk=request.GET['water'])
            if not waters.exists():
                raise WaterNotFoundException()
        else:
            waters = self.queryset.all()

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