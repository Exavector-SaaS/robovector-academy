from django.utils.deprecation import MiddlewareMixin


class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.organization = None

        org_slug = request.headers.get("X-ORG")
        if not org_slug:
            return

        from apps.core.models import Organization  # lazy import

        try:
            request.organization = Organization.objects.get(slug=org_slug)
        except Organization.DoesNotExist:
            request.organization = None
