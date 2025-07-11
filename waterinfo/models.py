from django.db import models

class Water(models.Model):
    """
    Describes a body of water (lake, river, etc)
    """
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128, default="")
    county = models.CharField(max_length=128, default="")
    state = models.CharField(max_length=50, default="")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    WaterType = [
        (0, "River"),
        (1, "Lake"),
        (2, "Resivoir"),
        (3, "Other"),
    ]
    water_type = models.SmallIntegerField(choices=WaterType, default=1)

    acres = models.FloatField(default=0)    # if we're given one of these we can calculate the other
    hectares = models.FloatField(default=0)
    max_depth_feet = models.PositiveSmallIntegerField(default=0) # we can calculate these, too
    max_depth_meters = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name