from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Launch

def index(request):
    latest_launch_list = Launch.objects.order_by("-date_updated")[:15]
    context = {"latest_launch_list": latest_launch_list}
    return render(request, "launchinfo/index.html", context)

def detail(request, launch_id):
    launch = get_object_or_404(Launch, pk=launch_id)
    return render(request, "launchinfo/detail.html", {"launch": launch})