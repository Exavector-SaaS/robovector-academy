from rest_framework.viewsets import ModelViewSet


class TenantViewSet(ModelViewSet):
    def get_queryset(self):
        qs = super().get_queryset()

        org = getattr(self.request, "organization", None)
        if not org:
            return qs.none()

        manager = getattr(qs.model.objects, "for_request", None)

        if callable(manager):
            return manager(self.request)

        # HARD FAIL (important for security)
        return qs.none()
