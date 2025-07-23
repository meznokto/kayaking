from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('api/launchinfo/', include("launchinfo.urls")),
    path('api/waterinfo/', include("waterinfo.urls")),
    path('api/tripinfo/', include("tripinfo.urls")),
    path('api/users/', include("users.urls")),
    path('api/util/', include("kayakutils.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
