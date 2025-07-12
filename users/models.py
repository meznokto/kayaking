from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

import os
import uuid

from launchinfo.models import Country, State, County, City

from .managers import KayakUserManager

def generate_unique_avatar_name(instance, filename):
    # Generate a unique filename using UUID and preserve the extension
    ext = filename.split('.')[-1]  # Get the file extension
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    return os.path.join('avatars', unique_name)

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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, db_constraint=False)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, db_constraint=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, db_constraint=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, db_constraint=False)
    signup_date = models.DateTimeField(default=timezone.now)
    birthday = models.DateField(blank=True, null=True)
    avatar = ProcessedImageField(upload_to=generate_unique_avatar_name, processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60}, default="noone.jpg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = KayakUserManager()

    def __str__(self):
        return self.display_name