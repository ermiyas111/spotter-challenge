from typing import Iterable, Tuple

from django.conf import settings

from shared.utils.geo import bounds_for_points, distance_point_to_polyline_miles
from stations.models import FuelStation


def get_stations_in_corridor(points: Iterable[Tuple[float, float]]) -> list[FuelStation]:
    route_points = list(points)
    min_lat, max_lat, min_lon, max_lon = bounds_for_points(route_points, settings.CORRIDOR_WIDTH_MILES)
    candidates = FuelStation.objects.filter(
        latitude__gte=min_lat,
        latitude__lte=max_lat,
        longitude__gte=min_lon,
        longitude__lte=max_lon,
    ).order_by("rack_price", "id")

    filtered: list[FuelStation] = []
    for station in candidates:
        distance = distance_point_to_polyline_miles(
            (float(station.latitude), float(station.longitude)),
            route_points,
        )
        if distance <= settings.CORRIDOR_WIDTH_MILES:
            filtered.append(station)

    return filtered
