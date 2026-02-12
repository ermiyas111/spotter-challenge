import uuid

from django.db import models
from django.utils import timezone


class TripRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    requested_at = models.DateTimeField(default=timezone.now)
    routing_provider = models.CharField(max_length=64)
    response_ms = models.PositiveIntegerField()
