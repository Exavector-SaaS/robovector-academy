from django.db import models
from apps.core.models import BaseTenantModel


class Course(BaseTenantModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Module(BaseTenantModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Lesson(BaseTenantModel):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
