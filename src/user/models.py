from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..core.models import BomBaseModel

class Department(models.Model):
    # NAME_CHOISE = [
    #     ("کمپرسور", "کمپرسور"),
    #     ("فن و کمپرسور", "فن و کمپرسور"),
    #     ("جانبی", "جانبی"),
    #     ("توربین", "توربین"),
    #     ("ماینور پارت", "ماینور پارت"),
    #     ("محفظه احتراق", "محفظه احتراق"),
    #     ("طراحي سازه موتور", "طراحي سازه موتور"),
    #     ("استاندارد و كيفيت", "استاندارد و كيفيت"),
    # ]
    name = models.CharField(null=True, blank=True, max_length=64)

    def __str__(self):
        return self.name
    

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
    
class HiddenColumns(models.Model):
    hidden_cols = models.JSONField(null=True, blank=True, default=dict)
    user = models.OneToOneField(BomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} : {self.hidden_cols}"
