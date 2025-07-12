from django.db import models # type: ignore
from django.utils import timezone # type: ignore

from waterinfo.models import Water
from kayakutils.models import Country, State, County, City
    
class Launch(models.Model):
    """
    Describes a boat launch (location, facilities, etc)
    """
    name = models.CharField(max_length=128)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    body_of_water = models.ForeignKey(Water, on_delete=models.SET_NULL, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    BathroomType = [
        (0, "None"),            # no bathrooms
        (1, "Outhouse"),        # outhouse/pit
        (2, "Plumbed"),         # running water
        (3, "Nearby"),          # neaby bathroom (convenience store, campground, etc)
    ]
    bathroom_type = models.SmallIntegerField(choices=BathroomType, default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=0) # number of bathrooms/stalls
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
    
