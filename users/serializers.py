from rest_framework import serializers # type: ignore

from .models import KayakUser

class KayakUsersSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    display_name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=128, allow_blank=True)
    last_name = serializers.CharField(max_length=256, allow_blank=True)
    email = serializers.EmailField()
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    county = serializers.PrimaryKeyRelatedField(read_only=True)
    state = serializers.PrimaryKeyRelatedField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(read_only=True)
    signup_date = serializers.DateTimeField(read_only=True)
    birthday = serializers.DateField(allow_null=True, required=False)
    avatar_url = serializers.URLField(source='avatar.url', read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                
    def create(self, validated_data):
        return KayakUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    