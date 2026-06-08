from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel


class CustomUser(AbstractUser, TimeStampedModel):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
