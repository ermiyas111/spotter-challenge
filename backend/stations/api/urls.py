from django.urls import path

from stations.api.views import FuelImportView

urlpatterns = [
    path("fuel-data/import", FuelImportView.as_view(), name="fuel-data-import"),
]
