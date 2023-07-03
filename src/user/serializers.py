from rest_framework import serializers

from .models import BomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = BomUser
        exclude = (
            "is_staff",
            "is_superuser",
            "is_active",
            "editable",
            "deletable",
            "deleted",
            "last_login",
        )
        extra_kwargs = {"password": {"write_only": True}}
