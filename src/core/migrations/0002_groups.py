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

departments = [
    "کمپرسور",
    "فن",
    "جانبی",
    "توربین",
    "ماینور پارت",
    "محفظه احتراق",
    "طراحي سازه موتور",
    "استاندارد و كيفيت",
]


def create_default_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Department = apps.get_model("user", "Department")

    for department in departments:
        Department.objects.create(name=department)

    for group in groups:
        Group.objects.create(name=group)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_admin"),
    ]

    operations = [
        migrations.RunPython(create_default_group),
    ]
