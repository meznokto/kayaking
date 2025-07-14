from django.urls import path

from .views import ListLaunches

urlpatterns = [
    path('', ListLaunches.as_view(), name='list_launches'),
    #path("", views.index, name="index"),
    #path("<int:launch_id>/", views.launchdetail, name="launchdetail"),
]