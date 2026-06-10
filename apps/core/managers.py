from django.db import models
from apps.core.tenant_context import get_current_organization


class TenantQuerySet(models.QuerySet):
    def for_request(self, request):
        org = getattr(request, "organization", None)
        if not org:
            return self.none()
        return self.filter(organization=org)


class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_request(self, request):
        return self.get_queryset().for_request(request)

    def create(self, **kwargs):
        org = get_current_organization()

        if org and "organization" not in kwargs:
            kwargs["organization"] = org

        return super().create(**kwargs)

    def bulk_create(self, objs, **kwargs):
        org = get_current_organization()

        if org:
            for obj in objs:
                if not getattr(obj, "organization_id", None):
                    obj.organization = org

        return super().bulk_create(objs, **kwargs)
