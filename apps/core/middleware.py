from apps.core.models import Organization
from apps.core.tenant_context import (
    set_current_organization,
    clear_current_organization,
)


class OrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        clear_current_organization()
        request.organization = None

        org_slug = request.headers.get("X-ORG")

        if not org_slug:
            return self.get_response(request)

        try:
            org = Organization.objects.get(slug=org_slug)

            # bind only if user is authenticated and member
            if (
                request.user.is_authenticated
                and request.user.memberships.filter(
                    organization=org, is_active=True
                ).exists()
            ):
                request.organization = org
                set_current_organization(org)

        except Organization.DoesNotExist:
            pass

        response = self.get_response(request)

        clear_current_organization()

        return response
