from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..core.models import BomBaseModel


class BomUser(AbstractUser):
    # avatar = models.ImageField(
    #     upload_to="core/UploadedFiles/avatars", null=True, blank=True
    # )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="bomuser_groups",
    )

    def __str__(self):
        return self.username
