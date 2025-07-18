from rest_framework import serializers # type: ignore

from tripinfo.models import Trip, TripImage
from waterinfo.serializers import WaterImageSerializer
from launchinfo.serializers import WaterSerializer, TripLaunchSerializer
from users.models import KayakUser

class TripImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripImage
        fields = ['id', 'original']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KayakUser
        fields = ['id', 'display_name']

class TripSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    #is_private = models.BooleanField(default=False)
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    body_of_water = WaterSerializer(read_only=True)
    start_launch = TripLaunchSerializer(read_only=True)
    end_launch = TripLaunchSerializer(read_only=True)
    images = TripImageSerializer(many=True, read_only=True)
    notes = serializers.CharField(default="", allow_blank=True, required=False)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create(self, validated_data):
        return Trip.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance