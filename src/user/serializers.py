from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import BomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = BomUser
        exclude = (
            "user_permissions",
            # "groups",
            "is_staff",
            "is_superuser",
            "is_active",
            "last_login",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = BomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "username",
            "groups",
        )
        # extra_kwargs = {"password": {"read_only": True}}


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", "id")
