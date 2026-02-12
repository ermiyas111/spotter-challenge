from __future__ import annotations

from math import cos, radians
from typing import Iterable, Tuple


MILES_PER_LAT_DEGREE = 69.0


def miles_to_lat_degrees(miles: float) -> float:
    return miles / MILES_PER_LAT_DEGREE


def miles_to_lon_degrees(latitude: float, miles: float) -> float:
    return miles / (MILES_PER_LAT_DEGREE * max(cos(radians(latitude)), 0.0001))


def miles_per_lon_degree(latitude: float) -> float:
    return MILES_PER_LAT_DEGREE * max(cos(radians(latitude)), 0.0001)


def bounds_for_points(points: Iterable[Tuple[float, float]], corridor_miles: float) -> tuple[float, float, float, float]:
    latitudes = [lat for lat, _ in points]
    longitudes = [lon for _, lon in points]
    if not latitudes or not longitudes:
        raise ValueError("Route geometry is empty")

    min_lat = min(latitudes)
    max_lat = max(latitudes)
    min_lon = min(longitudes)
    max_lon = max(longitudes)

    lat_buffer = miles_to_lat_degrees(corridor_miles)
    mean_lat = (min_lat + max_lat) / 2.0
    lon_buffer = miles_to_lon_degrees(mean_lat, corridor_miles)

    return (
        min_lat - lat_buffer,
        max_lat + lat_buffer,
        min_lon - lon_buffer,
        max_lon + lon_buffer,
    )


def distance_point_to_polyline_miles(
    point: Tuple[float, float],
    polyline: Iterable[Tuple[float, float]],
) -> float:
    distance, _position = closest_point_along_polyline_miles(point, polyline)
    return distance


def closest_point_along_polyline_miles(
    point: Tuple[float, float],
    polyline: Iterable[Tuple[float, float]],
) -> tuple[float, float]:
    points = list(polyline)
    if not points:
        raise ValueError("Route geometry is empty")
    if len(points) == 1:
        return _distance_point_to_point_miles(point, points[0]), 0.0

    cumulative: list[float] = [0.0]
    for start, end in zip(points, points[1:]):
        cumulative.append(cumulative[-1] + _distance_point_to_point_miles(start, end))

    min_distance = float("inf")
    best_position = 0.0
    for index, (start, end) in enumerate(zip(points, points[1:])):
        distance, segment_offset = _distance_point_to_segment_miles(point, start, end, with_offset=True)
        if distance < min_distance:
            min_distance = distance
            best_position = cumulative[index] + segment_offset

    return min_distance, best_position


def _distance_point_to_point_miles(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    lat1, lon1 = a
    lat2, lon2 = b
    mean_lat = (lat1 + lat2) / 2.0
    dx = (lon2 - lon1) * miles_per_lon_degree(mean_lat)
    dy = (lat2 - lat1) * MILES_PER_LAT_DEGREE
    return (dx * dx + dy * dy) ** 0.5


def _distance_point_to_segment_miles(
    point: Tuple[float, float],
    start: Tuple[float, float],
    end: Tuple[float, float],
    *,
    with_offset: bool = False,
) -> float | tuple[float, float]:
    lat_p, lon_p = point
    lat1, lon1 = start
    lat2, lon2 = end
    mean_lat = (lat1 + lat2 + lat_p) / 3.0

    x1 = lon1 * miles_per_lon_degree(mean_lat)
    y1 = lat1 * MILES_PER_LAT_DEGREE
    x2 = lon2 * miles_per_lon_degree(mean_lat)
    y2 = lat2 * MILES_PER_LAT_DEGREE
    xp = lon_p * miles_per_lon_degree(mean_lat)
    yp = lat_p * MILES_PER_LAT_DEGREE

    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        distance = ((xp - x1) ** 2 + (yp - y1) ** 2) ** 0.5
        if with_offset:
            return distance, 0.0
        return distance

    t = ((xp - x1) * dx + (yp - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    distance = ((xp - closest_x) ** 2 + (yp - closest_y) ** 2) ** 0.5
    if with_offset:
        segment_length = (dx * dx + dy * dy) ** 0.5
        return distance, t * segment_length
    return distance
