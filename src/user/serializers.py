from rest_framework import serializers

from .models import BomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = BomUser
        exclude = (
            "user_permissions",
            "groups",
            "is_staff",
            "is_superuser",
            "is_active",
            "editable",
            "deletable",
            "deleted",
            "last_login",
        )
        extra_kwargs = {"password": {"write_only": True}}
