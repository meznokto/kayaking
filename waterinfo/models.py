from django.db import models # type: ignore
from django.utils import timezone # type: ignore

from kayakutils.models import Country, State, County, City

class Water(models.Model):
    """
    Describes a body of water (lake, river, etc)
    """
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    WaterType = [
        (0, "River"),
        (1, "Lake"),
        (2, "Resivoir"),
        (3, "Other"),
    ]
    water_type = models.SmallIntegerField(choices=WaterType, default=1)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    acres = models.FloatField(default=0)    # if we're given one of these we can calculate the other
    hectares = models.FloatField(default=0)
    max_depth_feet = models.PositiveSmallIntegerField(default=0) # we can calculate these, too
    max_depth_meters = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def dms_latitude(self):
        is_positive = self.latitude >= 0
        latitude = abs(self.latitude)
        minutes,seconds = divmod(latitude*3600,60)
        degrees,minutes = divmod(minutes,60)
        degrees = degrees if is_positive else -degrees
        return (degrees,minutes,int(seconds))
    
    def dms_longitude(self):
        is_positive = self.longitude >= 0
        longitude = abs(self.longitude)
        minutes,seconds = divmod(longitude*3600,60)
        degrees,minutes = divmod(minutes,60)
        degrees = degrees if is_positive else -degrees
        return (degrees,minutes,int(seconds))