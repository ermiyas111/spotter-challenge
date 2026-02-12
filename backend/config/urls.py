from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("routing.api.urls")),
    path("api/", include("stations.api.urls")),
]
