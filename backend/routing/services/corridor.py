from typing import Iterable, Tuple

from stations.services.station_query import get_stations_in_corridor


def find_candidate_stations(route_points: Iterable[Tuple[float, float]]):
    return get_stations_in_corridor(route_points)
