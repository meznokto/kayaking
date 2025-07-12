from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from launchinfo.models import Country, State, County, City

from .managers import KayakUserManager

class KayakUser(AbstractBaseUser, PermissionsMixin):
    """
    Describes a user.
    """
    display_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    signup_date = models.DateTimeField(default=timezone.now)
    birthday = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='images/', default="nopicture.jpg")
    thumbnail = ImageSpecField(source='picture', processors=[ResizeToFill(100, 50)], format='JPEG', options={'quality': 60})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = KayakUserManager()

    def __str__(self):
        return self.display_name