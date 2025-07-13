from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from datetime import date

from waterinfo.models import Water
from launchinfo.models import Launch
from users.models import KayakUser

def generate_unique_trip_name(instance, filename):
    # Generate a unique filename using UUID and preserve the extension
    ext = filename.split('.')[-1]  # Get the file extension
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('trips', unique_name)

class Trip(models.Model):
    """
    Describes a trip taken on a body of water.
    """
    user = models.ForeignKey(KayakUser, on_delete=models.DO_NOTHING, default=1)
    is_private = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    body_of_water = models.ForeignKey(Water, on_delete=models.DO_NOTHING, null=True)
    start_launch = models.ForeignKey(Launch, on_delete=models.DO_NOTHING, related_name="trip_start_launch", null=True)
    end_launch = models.ForeignKey(Launch, on_delete=models.DO_NOTHING, related_name="trip_end_launch", null=True)
    notes = models.TextField(default="")

    def __str__(self):
        return self.body_of_water.name + " - " + date.strftime(self.start_time, '%d %b %Y')

class TripImage(models.Model):
    original = models.ImageField(upload_to=generate_unique_trip_name)
    thumbnail = ImageSpecField(source='original', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)