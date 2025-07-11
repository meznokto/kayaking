from django.db import models

class Water(models.Model):
    """
    Describes a body of water (lake, river, etc)
    """
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128, default="")
    county = models.CharField(max_length=128, default="")
    state = models.CharField(max_length=50, default="")

    WaterType = [
        (0, "River"),
        (1, "Lake"),
        (2, "Other"),
    ]
    water_type = models.SmallIntegerField(choices=WaterType, default=1)

    acres = models.FloatField(default=0)

    def __str__(self):
        return self.name