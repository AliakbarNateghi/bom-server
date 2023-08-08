import os

import pandas as pd
from django.contrib.auth import get_user_model
from django.db import migrations, transaction

script_dir = os.path.dirname(os.path.abspath(__file__))


def create_superuser(apps, schema_editor):
    User = get_user_model()

    with transaction.atomic():
        User.objects.create_superuser(username="admin", password="1234")


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
