import os

import pandas as pd
from django.contrib.auth import get_user_model
from django.db import migrations, transaction

script_dir = os.path.dirname(os.path.abspath(__file__))


def create_superuser(apps, schema_editor):
    User = get_user_model()
    hidden_cols = apps.get_model("user", "HiddenColumns")
    user = apps.get_model("user", "BomUser")

    with transaction.atomic():
        User.objects.create_superuser(username="admin", password="1234")
        user = user.objects.get(username="admin")
        hidden_cols.objects.create(user=user, hidden_cols={})


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
