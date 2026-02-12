from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from django.conf import settings

from stations.models import FuelStation
from shared.utils.geo import closest_point_along_polyline_miles


@dataclass
class FuelStopPlan:
    station: FuelStation
    stop_order: int
    distance_from_previous: float


@dataclass
class _StationPosition:
    station: FuelStation
    position_miles: float


def _max_leg_distance() -> float:
    return 500.0 - settings.SAFETY_BUFFER_MILES


def plan_fuel_stops(
    stations: Iterable[FuelStation],
    total_distance_miles: float,
    route_points: Iterable[tuple[float, float]],
) -> list[FuelStopPlan]:
    remaining = total_distance_miles
    stops: list[FuelStopPlan] = []
    reachable = _max_leg_distance()
    ordered = list(stations)
    route_points_list = list(route_points)
    station_positions: list[_StationPosition] = []

    for station in ordered:
        distance_to_route, position_miles = closest_point_along_polyline_miles(
            (float(station.latitude), float(station.longitude)),
            route_points_list,
        )
        if distance_to_route <= settings.CORRIDOR_WIDTH_MILES:
            station_positions.append(_StationPosition(station=station, position_miles=position_miles))

    station_positions.sort(key=lambda item: item.position_miles)

    if total_distance_miles <= reachable:
        return stops

    current_position = 0.0
    start_index = 0
    while remaining > reachable:
        while start_index < len(station_positions) and station_positions[start_index].position_miles <= current_position:
            start_index += 1

        end_index = start_index
        while end_index < len(station_positions) and station_positions[end_index].position_miles <= current_position + reachable:
            end_index += 1

        candidates = station_positions[start_index:end_index]
        if not candidates:
            raise ValueError("No reachable fuel stations within corridor")

        chosen = min(
            candidates,
            key=lambda item: (
                item.station.rack_price,
                item.position_miles,
                str(item.station.id),
            ),
        )
        leg_distance = chosen.position_miles - current_position
        stops.append(
            FuelStopPlan(
                station=chosen.station,
                stop_order=len(stops) + 1,
                distance_from_previous=leg_distance,
            )
        )
        current_position = chosen.position_miles
        remaining = total_distance_miles - current_position
        # print(
        #     "Candidate list:",
        #     [(c.station.rack_price, c.position_miles) for c in candidates]
        # )
        # print("Chosen: ", chosen.station.rack_price)
        # print("Current Position: ", current_position)
        # print("Remaining: ", remaining)

    return stops
