from routing.models import TripRequest


def record_trip_request(
    *,
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    routing_provider: str,
    response_ms: int,
) -> TripRequest:
    return TripRequest.objects.create(
        start_latitude=start_lat,
        start_longitude=start_lon,
        end_latitude=end_lat,
        end_longitude=end_lon,
        routing_provider=routing_provider,
        response_ms=response_ms,
    )
