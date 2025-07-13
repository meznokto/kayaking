from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Trip, TripImage

def index(request):
    latest_trip_list = Trip.objects.order_by("-date_updated")[:15]
    context = {"latest_trip_list": latest_trip_list}
    return render(request, "tripinfo/index.html", context)

def detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    pictures = TripImage.objects.filter(trip = trip_id)
    return render(request, "tripinfo/detail.html", {"trip": trip, "pictures": pictures})