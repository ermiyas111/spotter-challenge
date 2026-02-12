from decimal import Decimal
from time import perf_counter

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from routing.api.serializers import RoutePlanRequestSerializer, RoutePlanResponseSerializer
from routing.services.route_planner import compute_route_plan
from routing.services.request_log import record_trip_request
from shared.utils.errors import error_response


class RoutePlanView(APIView):
    def post(self, request):
        serializer = RoutePlanRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start = serializer.validated_data["start"]
        end = serializer.validated_data["end"]

        start_time = perf_counter()
        try:
            result = compute_route_plan(start["lat"], start["lon"], end["lat"], end["lon"])
        except ValueError as exc:
            return error_response(
                error="no_feasible_plan",
                message=str(exc),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        duration_ms = int((perf_counter() - start_time) * 1000)

        record_trip_request(
            start_lat=start["lat"],
            start_lon=start["lon"],
            end_lat=end["lat"],
            end_lon=end["lon"],
            routing_provider=settings.ROUTING_API_BASE_URL,
            response_ms=duration_ms,
        )

        payload = {
            "route_distance_miles": result.route_distance_miles,
            "total_fuel_cost": _total_cost(result.fuel_stops),
            "map_polyline": result.map_polyline,
            "fuel_stops": [
                {
                    "station_id": stop.station.id,
                    "station_name": stop.station.name,
                    "lat": float(stop.station.latitude),
                    "lon": float(stop.station.longitude),
                    "rack_price": stop.station.rack_price,
                    "stop_order": stop.stop_order,
                    "distance_from_previous_miles": stop.distance_from_previous,
                }
                for stop in result.fuel_stops
            ],
        }
        response = RoutePlanResponseSerializer(payload)
        return Response(response.data, status=status.HTTP_200_OK)


def _total_cost(stops) -> float:
    if not stops:
        return 0.0
    gallons_per_leg = (Decimal("500.0") - Decimal(str(settings.SAFETY_BUFFER_MILES))) / Decimal("10")
    total = sum(stop.station.rack_price * gallons_per_leg for stop in stops)
    return float(total)
