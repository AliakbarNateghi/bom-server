from django.db import migrations


def create_god_permissions(apps, schema_editor):
    FieldPermission = apps.get_model("component", "FieldPermission")
    BomComponent = apps.get_model("component", "BomComponent")
    Group = apps.get_model("auth", "Group")
    god = Group.objects.get(id=1)
    field_names = [field.name for field in BomComponent._meta.get_fields()]
    count = BomComponent.objects.count()
    for i in range(1, count + 1):
        for field_name in field_names:
            FieldPermission.objects.create(
                instance_id=i, editable=True, group=god, field=field_name
            )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_component_excel"),
    ]

    operations = [
        migrations.RunPython(create_god_permissions),
    ]
