import json
from urllib import parse, request

from django.conf import settings


class GeocodingClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.GEOCODING_API_BASE_URL).rstrip("/")

    def geocode_city_state(self, city: str, state: str) -> tuple[float, float]:
        query = parse.urlencode({"q": f"{city}, {state}, USA", "format": "json", "limit": 1})
        url = f"{self.base_url}/search?{query}"
        with request.urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if not payload:
            raise ValueError("Geocoding returned no results")

        entry = payload[0]
        return float(entry["lat"]), float(entry["lon"])
