from rest_framework import serializers


class FuelImportRequestSerializer(serializers.Serializer):
    csv_path = serializers.CharField()


class FuelImportResponseSerializer(serializers.Serializer):
    import_id = serializers.UUIDField()
    status = serializers.CharField()
