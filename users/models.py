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
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    signup_date = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = ProcessedImageField(upload_to=generate_unique_avatar_name, processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60}, default="noone.jpg")
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Kayak User"
        verbose_name_plural = "Kayak Users"
        ordering = ['display_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.display_name

    @property
    def is_authenticated(self):
        return True  # Always returns True for authenticated users

    @property
    def is_anonymous(self):
        return False  # Always returns False for authenticated users

    @property
    def name(self):
        return self.display_name

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    @property
    def profile_url(self):
        return f"/users/{self.id}/"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = KayakUserManager()

    def __str__(self):
        return self.display_name