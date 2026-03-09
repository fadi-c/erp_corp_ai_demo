from django.contrib import admin
from django.urls import path
from api.router import api
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", include("django_prometheus.urls")),
]