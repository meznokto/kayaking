from rest_framework import serializers

from waterinfo.models import Water
from kayakutils.models import Country, State, County, City
from launchinfo.models import Launch, LaunchImage

from launchinfo.serializers import CitySerializer, StateSerializer, CountySerializer, CountrySerializer

class WaterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchImage
        fields = ['id', 'original']

class WaterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0)
    main_image = WaterImageSerializer(read_only=True)
    thumbnail = serializers.ReadOnlyField(source="main_image.thumbnail.url")
    water_type = serializers.ChoiceField(choices=[
        (0, "River"),
        (1, "Lake"),
        (2, "Resivoir"),
        (3, "Other"),
    ], default=0)
    water_type_text = serializers.CharField(source='get_water_type_display', read_only=True)
    city = CitySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
