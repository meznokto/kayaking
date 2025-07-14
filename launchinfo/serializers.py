from rest_framework import serializers

from waterinfo.models import Water
from kayakutils.models import Country, State, County, City
from launchinfo.models import Launch, LaunchImage

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['id', 'name'] 

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class WaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Water
        fields = ['id', 'name']

class LaunchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchImage
        fields = ['id', 'original']

class BathroomTypeSerializer(serializers.Serializer):
    bathroom_display = serializers.CharField(source='get_bathroom_choices_display', read_only=True)
    class Meta:
        model = Launch
        fields = ('id', 'bathroom_display')

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
    #main_image = LaunchImageSerializer(read_only=True)
    main_image = LaunchImageSerializer(read_only=True)
    #bathroom_type = BathroomTypeSerializer(read_only=True)
    bathroom_type = serializers.ChoiceField(choices=[
        (0, "None"),
        (1, "Outhouse"),
        (2, "Plumbed"),
        (3, "Nearby"),
    ], default=0)
    bathrooms = serializers.IntegerField(default=0)
    bathroom_desc = serializers.CharField(allow_blank=True, allow_null=True)

    ramp_type = serializers.ChoiceField(choices=[
        (0, "None"),
        (1, "Hard Surfaced"),
        (2, "Carry Down"),
        (3, "Gravel"),
    ], default=1)

    parking_type = serializers.ChoiceField(choices=[
        (0, "None"),
        (1, "Gravel"),
        (2, "Paved"),
    ], default=1)
    pay_parking = serializers.BooleanField(default=False)
    pay_info = serializers.CharField(allow_blank=True, allow_null=True)

    comment = serializers.CharField(allow_blank=True, allow_null=True)

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