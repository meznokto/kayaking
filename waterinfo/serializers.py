from rest_framework import serializers # type: ignore

from waterinfo.models import Water, WaterImage
from kayakutils.serializers import CountrySerializer, StateSerializer, CountySerializer, CitySerializer

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Water
        fields = ['id', 'name']

class WaterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterImage
        fields = ['id', 'original']


class WaterSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    state = StateSerializer()
    county = CountySerializer()
    city = CitySerializer()
    
    class Meta:
        model = Water
        fields = ['id', 'name', 'date_created', 'date_updated',
                  'latitude', 'longitude', 'water_type',
                  'city', 'county', 'state', 'country', 
                  'acres', 'hectares', 'max_depth_feet', 'max_depth_meters'] 

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    
