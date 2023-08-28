from django.db import migrations


def create_god_permissions(apps, schema_editor):
    BomFieldPermission = apps.get_model("component", "BomFieldPermission")
    BomComponent = apps.get_model("component", "BomComponent")
    ProvideFieldPermission = apps.get_model("component", "ProvideFieldPermission")
    ProvideComponent = apps.get_model("component", "ProvideComponent")
    Group = apps.get_model("auth", "Group")
    god = Group.objects.get(id=1)

    field_names = [
        field.name
        for field in BomComponent._meta.get_fields()
        if field.name not in ["id", "deleted", "deletable"]
    ]
    field_permissions = [
        BomFieldPermission(instance_id=i, editable=True, group=god, field=field_name)
        for i in range(1, BomComponent.objects.count() + 1)
        for field_name in field_names
    ]
    BomFieldPermission.objects.bulk_create(field_permissions)

    field_names = [
        field.name
        for field in ProvideComponent._meta.get_fields()
        if field.name not in ["id", "deleted", "deletable"]
    ]
    field_permissions = [
        ProvideFieldPermission(instance_id=i, editable=True, group=god, field=field_name)
        for i in range(1, ProvideComponent.objects.count() + 1)
        for field_name in field_names
    ]
    ProvideFieldPermission.objects.bulk_create(field_permissions)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_component"),
    ]

    operations = [
        migrations.RunPython(create_god_permissions),
    ]
