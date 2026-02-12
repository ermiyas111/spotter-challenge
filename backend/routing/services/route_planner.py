from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings

from routing.services.corridor import find_candidate_stations
from routing.services.osrm_client import OsrmClient
from routing.services.optimizer import plan_fuel_stops
from shared.utils.geo import bounds_for_points


@dataclass
class RoutePlanResult:
    route_distance_miles: float
    map_polyline: str
    fuel_stops: list


def compute_route_plan(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> RoutePlanResult:
    client = OsrmClient()
    route = client.get_route(start_lat, start_lon, end_lat, end_lon)
    route_distance_miles = route["distance_meters"] / 1609.34

    points = _decode_polyline(route["geometry"])
    _ = bounds_for_points(points, settings.CORRIDOR_WIDTH_MILES)

    stations = find_candidate_stations(points)
    fuel_stops = plan_fuel_stops(stations, route_distance_miles, points)

    return RoutePlanResult(
        route_distance_miles=route_distance_miles,
        map_polyline=route["geometry"],
        fuel_stops=fuel_stops,
    )


def _decode_polyline(polyline: str):
    index = 0
    lat = 0
    lon = 0
    coordinates = []

    while index < len(polyline):
        result = 0
        shift = 0
        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break
        delta_lat = ~(result >> 1) if result & 1 else result >> 1
        lat += delta_lat

        result = 0
        shift = 0
        while True:
            byte = ord(polyline[index]) - 63
            index += 1
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20:
                break
        delta_lon = ~(result >> 1) if result & 1 else result >> 1
        lon += delta_lon

        coordinates.append((lat / 1e5, lon / 1e5))

    return coordinates
