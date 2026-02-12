import uuid

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FuelDataImport",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("source_filename", models.CharField(max_length=255)),
                ("imported_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("row_count", models.PositiveIntegerField()),
                ("invalid_row_count", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        max_length=16,
                        choices=[("succeeded", "Succeeded"), ("failed", "Failed")],
                    ),
                ),
                ("notes", models.TextField(blank=True)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["imported_at"], name="fuelimport_time_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="FuelStation",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=128)),
                ("state", models.CharField(max_length=2)),
                ("latitude", models.DecimalField(max_digits=9, decimal_places=6)),
                ("longitude", models.DecimalField(max_digits=9, decimal_places=6)),
                ("rack_price", models.DecimalField(max_digits=8, decimal_places=3)),
                ("geocoded_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("geocode_source", models.CharField(max_length=64)),
                (
                    "data_import",
                    models.ForeignKey(
                        to="stations.fueldataimport",
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stations",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["state"], name="fuelstation_state_idx"),
                    models.Index(fields=["latitude"], name="fuelstation_lat_idx"),
                    models.Index(fields=["longitude"], name="fuelstation_lon_idx"),
                    models.Index(fields=["latitude", "longitude"], name="fuelstation_latlon_idx"),
                ],
            },
        ),
    ]
