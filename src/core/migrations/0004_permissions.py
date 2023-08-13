from django.db import migrations


def create_god_permissions(apps, schema_editor):
    FieldPermission = apps.get_model("component", "FieldPermission")
    BomComponent = apps.get_model("component", "BomComponent")
    Group = apps.get_model("auth", "Group")
    god = Group.objects.get(id=1)
    field_names = [
        field.name
        for field in BomComponent._meta.get_fields()
        if field.name not in ["id", "deleted", "deletable"]
    ]
    # field_permissions = []
    # for i in range(1, BomComponent.objects.count() + 1):
    #     for field_name in field_names:
    #         field_permissions.append(FieldPermission(instance_id=i, editable=True, group=god, field=field_name))
    field_permissions = [
        FieldPermission(instance_id=i, editable=True, group=god, field=field_name)
        for i in range(1, BomComponent.objects.count() + 1)
        for field_name in field_names
    ]
    FieldPermission.objects.bulk_create(field_permissions)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_component_excel"),
    ]

    operations = [
        migrations.RunPython(create_god_permissions),
    ]
