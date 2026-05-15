from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse


def health_check(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
    except OperationalError:
        return JsonResponse({"status": "unhealthy", "database": "unavailable"}, status=503)

    return JsonResponse({"status": "ok"})
