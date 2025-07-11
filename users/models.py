from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import KayakUserManager

class KayakUser(AbstractBaseUser, PermissionsMixin):
    """
    Describes a user.
    """
    display_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=128, default="")
    last_name = models.CharField(max_length=256, default="")
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    city = models.CharField(max_length=128, default="")
    county = models.CharField(max_length=128, default="")
    state = models.CharField(max_length=50, default="")
    signup_date = models.DateTimeField(default=timezone.now)
    birthday = models.DateField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = KayakUserManager()

    def __str__(self):
        return self.display_name