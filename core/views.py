from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    """
    Check if the service is running.
    """

    def get(self, request):
        return Response(
            {"status": "ok", "message": "Service is running"}, status=status.HTTP_200_OK
        )
