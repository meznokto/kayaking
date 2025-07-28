from rest_framework import serializers # type: ignore

from waterinfo.models import Water, WaterImage
from kayakutils.serializers import CountrySerializer, StateSerializer, CountySerializer, CitySerializer
from kayakutils.models import Country, State, County, City

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Water
        fields = ['id', 'name']

class WaterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterImage
        fields = ['id', 'original']

    
class WaterSerializer(serializers.ModelSerializer):
    #country = CountrySerializer(read_only=True)
    #state = StateSerializer(read_only=True)
    #county = CountySerializer(read_only=True)
    #city = CitySerializer(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    country_name = serializers.CharField(source='country.name', read_only=True)
    country_abbr = serializers.CharField(source='country.abbr', read_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_abbr = serializers.CharField(source='state.abbr', read_only=True)
    county = serializers.PrimaryKeyRelatedField(queryset=County.objects.all())
    county_name = serializers.CharField(source='county.name', read_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Water
        fields = [
            'id', 'name', 'date_created', 'date_updated',
            'latitude', 'longitude', 'water_type',
            'city', 'city_name', 'county', 'county_name', 
            'state', 'state_name', 'state_abbr', 'country', 'country_name', 'country_abbr',
            'acres', 'hectares', 'max_depth_feet', 'max_depth_meters', 'description'
        ]

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
