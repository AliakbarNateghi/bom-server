from rest_framework import serializers

from .models import BomComponent, FieldPermission


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomComponent
        exclude = [
            'id',
            'deleted',
            'deletable',
            'editable',
        ]


class FieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldPermission
        fields = '__all__'