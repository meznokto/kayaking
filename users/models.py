from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

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
    city = models.CharField(max_length=128, blank=True)
    county = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=50, blank=True)
    signup_date = models.DateTimeField(default=timezone.now)
    birthday = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='images/', default="nopicture.jpg")
    thumbnail = ImageSpecField(source='picture', processors=[ResizeToFill(100, 50)], format='JPEG', options={'quality': 60})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = KayakUserManager()

    def __str__(self):
        return self.display_name