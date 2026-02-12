from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from stations.api.serializers import FuelImportRequestSerializer, FuelImportResponseSerializer
from stations.services.csv_importer import import_fuel_csv
from shared.utils.errors import error_response


class FuelImportView(APIView):
    def post(self, request):
        serializer = FuelImportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data_import = import_fuel_csv(serializer.validated_data["csv_path"])
        except Exception as exc:
            return error_response(
                error="import_failed",
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        response = FuelImportResponseSerializer(
            {
                "import_id": data_import.id,
                "status": data_import.status,
            }
        )
        return Response(response.data, status=status.HTTP_202_ACCEPTED)
