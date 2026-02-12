import json
from urllib import parse, request

from django.conf import settings


class OsrmClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.ROUTING_API_BASE_URL).rstrip("/")

    def get_route(self, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> dict:
        coords = f"{start_lon},{start_lat};{end_lon},{end_lat}"
        query = parse.urlencode({"overview": "full", "geometries": "polyline", "steps": "false"})
        url = f"{self.base_url}/route/v1/driving/{coords}?{query}"
        with request.urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if payload.get("code") != "Ok" or not payload.get("routes"):
            raise ValueError("Routing provider returned no route")

        route = payload["routes"][0]
        return {
            "distance_meters": route.get("distance"),
            "duration_seconds": route.get("duration"),
            "geometry": route.get("geometry"),
        }
