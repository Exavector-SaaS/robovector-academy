import uuid
from django.db import models
from apps.core.managers import TenantManager


# =========================
# BASE MODEL
# =========================


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# =========================
# ORGANIZATION (TENANT ROOT)
# =========================


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# =========================
# BASE TENANT MODEL
# =========================


class BaseTenantModel(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="%(class)s_set"
    )

    objects = TenantManager()

    class Meta:
        abstract = True
