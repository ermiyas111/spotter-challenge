import csv
from pathlib import Path
from typing import Iterable

from django.db import transaction
from django.utils import timezone

from stations.models import FuelDataImport, FuelStation
from stations.services.geocoding import GeocodingClient


PRICE_FIELDS = ("Retail Price", "OPIS Price", "Rack Price", "rack_price", "op_iS_price")
NAME_FIELDS = ("Truckstop Name", "Name", "name")
OPIS_ID_FIELDS = ("OPIS Truckstop ID", "Truckstop ID", "opis_truckstop_id")
RACK_ID_FIELDS = ("Rack ID", "rack_id")


def _get_first_value(row: dict, keys: Iterable[str]) -> str | None:
    for key in keys:
        if key in row and row[key]:
            return row[key]
    return None


def import_fuel_csv(csv_path: str) -> FuelDataImport:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    geocoder = GeocodingClient()
    cache: dict[tuple[str, str], tuple[float, float]] = {}

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    invalid_rows = 0
    with transaction.atomic():
        data_import = FuelDataImport.objects.create(
            source_filename=path.name,
            imported_at=timezone.now(),
            row_count=len(rows),
            invalid_row_count=0,
            status=FuelDataImport.STATUS_SUCCEEDED,
        )

        for row in rows:
            try:
                name = _get_first_value(row, NAME_FIELDS)
                address = row.get("Address") or ""
                city = row.get("City") or ""
                state = row.get("State") or ""
                opis_truckstop_id = _get_first_value(row, OPIS_ID_FIELDS) or ""
                rack_id = _get_first_value(row, RACK_ID_FIELDS) or ""
                price_raw = _get_first_value(row, PRICE_FIELDS)

                if not name or not city or not state or price_raw is None:
                    raise ValueError("Missing required fields")

                rack_price = float(price_raw)

                key = (city.strip().lower(), state.strip().upper())
                if key in cache:
                    latitude, longitude = cache[key]
                else:
                    latitude, longitude = geocoder.geocode_city_state(city, state)
                    cache[key] = (latitude, longitude)

                station, _created = FuelStation.objects.update_or_create(
                    name=name.strip(),
                    address=address.strip(),
                    city=city.strip(),
                    state=state.strip().upper(),
                    defaults={
                        "opis_truckstop_id": opis_truckstop_id.strip(),
                        "rack_id": rack_id.strip(),
                        "latitude": latitude,
                        "longitude": longitude,
                        "rack_price": rack_price,
                        "geocoded_at": timezone.now(),
                        "geocode_source": "nominatim",
                        "data_import": data_import,
                    },
                )
            except Exception:
                invalid_rows += 1
                continue

        data_import.invalid_row_count = invalid_rows
        if invalid_rows > 0:
            data_import.status = FuelDataImport.STATUS_FAILED
        data_import.save(update_fields=["invalid_row_count", "status"])

    return data_import
