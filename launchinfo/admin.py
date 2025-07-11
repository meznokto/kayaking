from django.contrib import admin

from .models import Launch, Water
from tripinfo.models import Trip

admin.site.register(Launch)
admin.site.register(Water)
admin.site.register(Trip)