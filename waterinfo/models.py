from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from kayakutils.models import Country, State, County, City

def generate_unique_water_name(instance, filename):
    # Generate a unique filename using UUID and preserve the extension
    ext = filename.split('.')[-1]  # Get the file extension
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('waters', unique_name)

class Water(models.Model):
    """
    Describes a body of water (lake, river, etc)
    """
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
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
    max_depth_meters = models.DecimalField(decimal_places=1, max_digits=10, default=0)

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
    
class WaterImage(models.Model):
    original = models.ImageField(upload_to=generate_unique_water_name)
    thumbnail = ImageSpecField(source='original', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    water = models.ForeignKey(Water, on_delete=models.CASCADE)