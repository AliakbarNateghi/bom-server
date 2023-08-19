from rest_framework import serializers

from .models import BomComponent, FieldPermission


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomComponent
        # fields = "__all__"
        exclude = [
            # 'id',
            "deleted",
            "deletable",
            # 'editable',
        ]


class FieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldPermission
        fields = ["group", "field", "instance_id", "editable"]
        # fields = "__all__"


class MassPermissionSerializer(serializers.Serializer):
    field = serializers.CharField(required=True)
    group = serializers.IntegerField(required=True)
    editable = serializers.BooleanField(required=False)