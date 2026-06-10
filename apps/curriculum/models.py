from django.db import models
from apps.core.models import BaseTenantModel


class Course(BaseTenantModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
