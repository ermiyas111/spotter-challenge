from rest_framework import serializers


class CoordinateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()


class RoutePlanRequestSerializer(serializers.Serializer):
    start = CoordinateSerializer()
    end = CoordinateSerializer()


class FuelStopSerializer(serializers.Serializer):
    station_id = serializers.UUIDField()
    station_name = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    rack_price = serializers.DecimalField(max_digits=8, decimal_places=3)
    stop_order = serializers.IntegerField()
    distance_from_previous_miles = serializers.FloatField(required=False)


class RoutePlanResponseSerializer(serializers.Serializer):
    route_distance_miles = serializers.FloatField()
    total_fuel_cost = serializers.FloatField()
    map_polyline = serializers.CharField()
    fuel_stops = FuelStopSerializer(many=True)
