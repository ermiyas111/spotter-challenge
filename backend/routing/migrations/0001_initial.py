import uuid

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TripRequest",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("start_latitude", models.DecimalField(max_digits=9, decimal_places=6)),
                ("start_longitude", models.DecimalField(max_digits=9, decimal_places=6)),
                ("end_latitude", models.DecimalField(max_digits=9, decimal_places=6)),
                ("end_longitude", models.DecimalField(max_digits=9, decimal_places=6)),
                ("requested_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("routing_provider", models.CharField(max_length=64)),
                ("response_ms", models.PositiveIntegerField()),
            ],
        ),
    ]
