from django.db import models

class User(models.Model):
    """
    Describes a user.
    """
    display_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    city = models.CharField(max_length=128, default="")
    county = models.CharField(max_length=128, default="")
    state = models.CharField(max_length=50, default="")
    signup_date = models.DateTimeField(default=timezone.now)
    birthday = models.DateField(blank=True)