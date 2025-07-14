from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import os
import uuid

from waterinfo.models import Water
from kayakutils.models import Country, State, County, City
    
def generate_unique_launch_name(instance, filename):
    # Generate a unique filename using UUID and preserve the extension
    ext = filename.split('.')[-1]  # Get the file extension
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('launches', unique_name)

class Launch(models.Model):
    """
    Describes a boat launch (location, facilities, etc)
    """
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    body_of_water = models.ForeignKey(Water, on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    main_image = models.ForeignKey('launchinfo.LaunchImage', on_delete=models.SET_NULL, null=True, related_name="launch_main_image")

    BATHROOM_CHOICES = [
        (0, "None"),            # no bathrooms
        (1, "Outhouse"),        # outhouse/pit
        (2, "Plumbed"),         # running water
        (3, "Nearby"),          # neaby bathroom (convenience store, campground, etc)
    ]
    bathroom_type = models.SmallIntegerField(choices=BATHROOM_CHOICES, default=0)
    bathrooms = models.SmallIntegerField(default=0) # number of bathrooms/stalls
    bathroom_desc = models.TextField(null=True, blank=True) # short description, optional

    RampType = [
        (0, "None"),             # this shouldn't be needed, but just in case
        (1, "Hard Surfaced"),    # paved ramp
        (2, "Carry Down"),       # no ramp, but can carry boat to water
        (3, "Gravel"),           # gravel ramp
    ]
    ramp_type = models.SmallIntegerField(choices=RampType, default=1)

    ParkingType = [
        (0, "None"),             # no parking available
        (1, "Gravel"),           # gravel/dirt parking lot
        (2, "Paved"),            # paved parking lot
    ]
    parking_type = models.SmallIntegerField(choices=ParkingType, default=1)
    pay_parking = models.BooleanField(default=False)            # if payment is required to park
    pay_info = models.TextField(null=True, blank=True)    # payment details, if needed

    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class LaunchImage(models.Model):
    original = models.ImageField(upload_to=generate_unique_launch_name)
    thumbnail = ImageSpecField(source='original', processors=[ResizeToFit(200, 200)], format='JPEG', options={'quality': 60})
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)


    def __str__(self):
        return f"Image {self.id} for Launch {self.launch.name}" if self.launch else f"Image {self.id}"