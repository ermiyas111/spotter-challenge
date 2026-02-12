import uuid

from django.db import models
from django.utils import timezone


class FuelDataImport(models.Model):
    STATUS_SUCCEEDED = "succeeded"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_SUCCEEDED, "Succeeded"),
        (STATUS_FAILED, "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_filename = models.CharField(max_length=255)
    imported_at = models.DateTimeField(default=timezone.now)
    row_count = models.PositiveIntegerField()
    invalid_row_count = models.PositiveIntegerField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["imported_at"], name="fuelimport_time_idx"),
        ]


class FuelStation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    opis_truckstop_id = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    rack_id = models.CharField(max_length=32, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    rack_price = models.DecimalField(max_digits=8, decimal_places=3)
    geocoded_at = models.DateTimeField(default=timezone.now)
    geocode_source = models.CharField(max_length=64)
    data_import = models.ForeignKey(
        FuelDataImport,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stations",
    )

    class Meta:
        indexes = [
            models.Index(fields=["state"], name="fuelstation_state_idx"),
            models.Index(fields=["latitude"], name="fuelstation_lat_idx"),
            models.Index(fields=["longitude"], name="fuelstation_lon_idx"),
            models.Index(fields=["latitude", "longitude"], name="fuelstation_latlon_idx"),
        ]
