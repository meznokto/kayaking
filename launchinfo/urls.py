from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:launch_id>/", views.launchdetail, name="launchdetail"),
]