from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Water

def index(request):
    latest_water_list = Water.objects.order_by("-date_updated")[:15]
    context = {"latest_water_list": latest_water_list}
    return render(request, "waterinfo/index.html", context)

def detail(request, water_id):
    water = get_object_or_404(Water, pk=water_id)
    latitude = water.dms_latitude()
    longitude = water.dms_longitude()
    return render(request, "waterinfo/detail.html", {"water": water, "latitude": latitude, "longitude": longitude})