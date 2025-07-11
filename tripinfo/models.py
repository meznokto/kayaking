from django.db import models # type: ignore
from django.utils import timezone # type: ignore

from waterinfo.models import Water
from launchinfo.models import Launch

class Trip(models.Model):
    """
    Describes a trip taken on a body of water.
    """
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    body_of_water = models.ForeignKey(Water, on_delete=models.DO_NOTHING, null=True)
    start_launch = models.ForeignKey(Launch, on_delete=models.DO_NOTHING, related_name="trip_start_launch", null=True)
    end_launch = models.ForeignKey(Launch, on_delete=models.DO_NOTHING, related_name="trip_end_launch", null=True)
