import os
# from django.contrib.auth.models import Group
import pandas as pd
from django.contrib.auth import get_user_model
from django.db import migrations, transaction

script_dir = os.path.dirname(os.path.abspath(__file__))


def create_superuser(apps, schema_editor):
    User = get_user_model()
    Group = apps.get_model("auth", "Group")
    god = Group.objects.filter(name="god")
    hidden_cols = apps.get_model("user", "HiddenColumns")
    user = apps.get_model("user", "BomUser")

    with transaction.atomic():
        User.objects.create_superuser(username="admin", password="1234")
        user = user.objects.get(username="admin")
        user.groups.set(list(god))
        hidden_cols.objects.create(user=user, hidden_cols={})


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_groups"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
