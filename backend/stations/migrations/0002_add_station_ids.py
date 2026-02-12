from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fuelstation",
            name="opis_truckstop_id",
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AddField(
            model_name="fuelstation",
            name="rack_id",
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
