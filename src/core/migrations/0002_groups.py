from django.db import migrations

groups = [
    "god",
    "design admin",
    "design fan and compressor",
    "design turbine",
    "design combustion",
    "design other",
    "build admin",
    "build fan and compressor",
    "build turbine",
    "build combustion",
    "build other",
    "quality admin",
    "quality normal",
    "supply admin",
    "supply contracts",
    "supply internal",
    "supply external",
    "financial currency",
    "financial rial",
    "accessories admin",
    "accessories normal",
]


def create_default_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    for group in groups:
        Group.objects.create(name=group)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_admin"),
    ]

    operations = [
        migrations.RunPython(create_default_group),
    ]
