from rest_framework import serializers

from launchinfo.models import Launch, LaunchImage
from waterinfo.serializers import WaterSerializer
from kayakutils.serializers import CountrySerializer, CountySerializer, StateSerializer, CitySerializer

class LaunchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchImage
        fields = ['id', 'original']

class LaunchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    date_created = serializers.DateTimeField(read_only=True)
    date_updated = serializers.DateTimeField(read_only=True)
    city = CitySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    body_of_water = WaterSerializer(read_only=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0)
    main_image = LaunchImageSerializer(read_only=True)
    thumbnail = serializers.ReadOnlyField(source="main_image.thumbnail.url")
    bathroom_type = serializers.ChoiceField(choices=[
        (0, "None"),
        (1, "Outhouse"),
        (2, "Plumbed"),
        (3, "Nearby"),
    ], default=0)
    bathroom_text = serializers.CharField(source='get_bathroom_type_display', read_only=True)
    
    bathrooms = serializers.IntegerField(default=0)
    bathroom_desc = serializers.CharField(allow_blank=True, allow_null=True)

    ramp_type = serializers.ChoiceField(choices=[
        (0, "None"),
        (1, "Hard Surfaced"),
        (2, "Carry Down"),
        (3, "Gravel"),
    ], default=1)
    ramp_text = serializers.CharField(source='get_ramp_type_display', read_only=True)

    parking_type = serializers.ChoiceField(choices=[
        (0, "None"),
        (1, "Gravel"),
        (2, "Paved"),
    ], default=1)
    parking_text = serializers.CharField(source='get_parking_type_display', read_only=True)

    pay_parking = serializers.BooleanField(default=False)
    pay_info = serializers.CharField(allow_blank=True, allow_null=True)

    comment = serializers.CharField(allow_blank=True, allow_null=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        return Launch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.county = validated_data.get('county', instance.county)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.body_of_water = validated_data.get('body_of_water', instance.body_of_water)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.main_image = validated_data.get('launch_main_image', instance.main_image)

        instance.bathroom_type = validated_data.get('bathroom_type', instance.bathroom_type)
        instance.bathrooms = validated_data.get('bathrooms', instance.bathrooms)
        instance.bathroom_desc = validated_data.get('bathroom_desc', instance.bathroom_desc)
        instance.ramp_type = validated_data.get('ramp_type', instance.ramp_type)
        instance.parking_type = validated_data.get('parking_type', instance.parking_type)
        instance.pay_parking = validated_data.get('pay_parking', instance.pay_parking)
        instance.pay_info = validated_data.get('pay_info', instance.pay_info)
        instance.comment = validated_data.get('comment', instance.comment)

        instance.save()
        return instance
    
class TripLaunchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, default=0)
    city = CitySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
