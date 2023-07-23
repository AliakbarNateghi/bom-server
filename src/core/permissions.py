from rest_framework import permissions
from django.contrib.auth.models import Group
from ..component.models import FieldPermission

class IsGod(permissions.BasePermission):
    def has_permission(self, request, view):
        god = Group.objects.get(name="god")
        return request.user if god in request.user.groups.all() else None
    

class TestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        groups = user.groups.all()
        # if request.method in permissions.SAFE_METHODS:
        #     field_permissions = FieldPermission.objects.


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
