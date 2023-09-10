from rest_framework import serializers

from .models import (
    BomComponent,
    BomFieldPermission,
    ProvideComponent,
    ProvideFieldPermission,
)


class BomComponentSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = BomComponent
        # fields = "__all__"
        exclude = [
            # 'id',
            "deleted",
            "deletable",
            # 'editable',
        ]


class ProvideComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvideComponent
        exclude = [
            # 'id',
            "deleted",
            "deletable",
            # 'editable',
        ]


class BomFieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomFieldPermission
        fields = ["group", "field", "instance_id", "editable"]


class ProvideFieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvideFieldPermission
        fields = ["group", "field", "instance_id", "editable"]


class MassPermissionSerializer(serializers.Serializer):
    field = serializers.CharField(required=True)
    group = serializers.IntegerField(required=True)
    editable = serializers.BooleanField(required=False, allow_null=True)
