from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from ..core.models import BomBaseModel


class BomUser(AbstractUser, BomBaseModel):
    avatar = models.ImageField(
        upload_to="core/UploadedFiles/avatars", null=True, blank=True
    )
    status = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.username
