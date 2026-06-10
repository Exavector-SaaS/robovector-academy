from rest_framework.viewsets import ModelViewSet


class TenantViewSet(ModelViewSet):
    def get_queryset(self):
        qs = super().get_queryset()

        organization = getattr(self.request, "organization", None)
        if not organization:
            return qs.none()

        return qs.filter(organization=organization)
