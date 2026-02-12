from rest_framework.response import Response


def error_response(*, error: str, message: str, status_code: int) -> Response:
    return Response({"error": error, "message": message}, status=status_code)
