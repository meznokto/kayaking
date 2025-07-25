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

    def create(self, validated_data):
        return Water.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
