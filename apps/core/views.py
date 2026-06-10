# Create your views here.
# apps/core/views.py
from django.http import JsonResponse


def debug_tenant(request):
    return JsonResponse(
        {"org": str(request.organization) if request.organization else None}
    )
