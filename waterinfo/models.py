from django.db import models # type: ignore

from kayakutils.models import Country, State, County, City

class Water(models.Model):
    """
    Describes a body of water (lake, river, etc)
    """
    name = models.CharField(max_length=128)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    WaterType = [
        (0, "River"),
        (1, "Lake"),
        (2, "Resivoir"),
        (3, "Other"),
    ]
    water_type = models.SmallIntegerField(choices=WaterType, default=1)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, db_constraint=False)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, db_constraint=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, db_constraint=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, db_constraint=False)
    acres = models.FloatField(default=0)    # if we're given one of these we can calculate the other
    hectares = models.FloatField(default=0)
    max_depth_feet = models.PositiveSmallIntegerField(default=0) # we can calculate these, too
    max_depth_meters = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name