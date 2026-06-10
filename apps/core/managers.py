from django.db import models


class TenantQuerySet(models.QuerySet):
    def for_request(self, request):
        organization = getattr(request, "organization", None)
        if not organization:
            return self.none()
        return self.filter(organization=organization)


class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_request(self, request):
        return self.get_queryset().for_request(request)

    def create(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        organization = getattr(request, "organization", None) if request else None

        if organization:
            kwargs["organization"] = organization

        return super().create(*args, **kwargs)
