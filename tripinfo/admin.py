from django.contrib import admin

from .models import Trip, TripImage

# Register your models here.
admin.site.register(Trip)
admin.site.register(TripImage)