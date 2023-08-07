import json

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..core.permissions import IsGod
from ..core.versatile_funcs import compare_instance_with_dict
from .models import BomComponent, FieldPermission
from .serializers import ComponentSerializer, FieldPermissionSerializer


def delete_common_keys_values(json_data, dictionary):
    json_dict = json.loads(json_data)
    common_keys = set(json_dict.keys()) & set(dictionary.keys())
    for key in common_keys:
        del json_dict[key]
    common_values = set(json_dict.values()) & set(dictionary.values())
    for key, value in json_dict.items():
        if value in common_values:
            del json_dict[key]
    modified_json = json.dumps(json_dict)
    return modified_json


class Component(ModelViewSet):
    queryset = BomComponent.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        groups = user.groups.all()
        instances = FieldPermission.objects.filter(group__in=groups)
        if not instances:
            return Response({"message": "you don't have access to see any field"})
        queryset_dict = {}
        for instance in instances:
            field_name = instance.field
            try:
                obj = BomComponent.objects.get(id=instance.instance_id)
                field_value = getattr(obj, field_name)
                if instance.instance_id not in queryset_dict:
                    queryset_dict[instance.instance_id] = {
                        "id": instance.instance_id,
                        # "editable": instance.editable,
                    }
                queryset_dict[instance.instance_id][field_name] = field_value
            except BomComponent.DoesNotExist:
                pass
        queryset_list = list(queryset_dict.values())
        print(f"queryset_dict: {queryset_dict}")
        print(f"queryset_list: {queryset_list}")
        return Response(queryset_list, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        obj = BomComponent.objects.get(id=pk)
        print(f"request.data : {request.data}")
        json_dict = request.data
        print(f"json_dict : {json_dict}")
        instances = FieldPermission.objects.filter(
            group__in=groups, editable=True, instance_id=pk
        )
        if not instances:
            return Response(
                {"message": "You don't have access to edit this particular cell"}
            )
        try:
            for instance in instances:
                for key, value in json_dict.items():
                    print(f"key : {key}, value: {value}")
                    print(f"instance.field: {instance.field}")
                    if instance.field == key and instance.editable:
                        data = {f"{key}": value}
                        serializer = self.get_serializer(obj, data=data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
        except:
            queryset_dict = {}
            for instance in instances:
                field_name = instance.field
                print(f"filed_name: {field_name}")
                try:
                    obj = BomComponent.objects.get(id=pk)
                    field_value = getattr(obj, field_name)
                    if instance.instance_id not in queryset_dict:
                        queryset_dict[instance.instance_id] = {
                            "id": instance.instance_id,
                            # "editable": instance.editable,
                        }
                    queryset_dict[instance.instance_id][field_name] = field_value
                    print(f"queryset_dict: {queryset_dict}")
                except BomComponent.DoesNotExist:
                    pass
            queryset_list = list(queryset_dict.values())
            print(f"queryset_list: {queryset_list}")
            false_type_response = {"message": "type problem", "data": queryset_list}
            return Response(false_type_response, status=status.HTTP_200_OK)
        queryset_dict = {}
        for instance in instances:
            field_name = instance.field
            print(f"filed_name: {field_name}")
            obj = BomComponent.objects.get(id=pk)
            try:
                field_value = getattr(obj, field_name)
                if instance.instance_id not in queryset_dict:
                    queryset_dict[instance.instance_id] = {
                        "id": instance.instance_id,
                    }
                queryset_dict[instance.instance_id][field_name] = field_value
                print(f"queryset_dict: {queryset_dict}")
            except BomComponent.DoesNotExist:
                pass
        print(f"obj : {type(obj)}")
        queryset_list = list(queryset_dict.values())
        print(f"queryset_list: {type(queryset_list[0])}")
        result = compare_instance_with_dict(obj, queryset_list[0])
        print(f"result : {result}")
        true_response = {
            "message": "permission problem" if result else "success",
            "data": queryset_list,
        }
        return Response(true_response, status=status.HTTP_200_OK)

        # return Response(serializer.data, status=status.HTTP_200_OK)
        # continue
        # return Response({"message": "Something is wrong"})

    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)

    # def create(self, request):
    #     user = request.user
    #     groups = user.groups.all()
    #     # permission to create a new object
    #     permissions = FieldPermission.objects.filter(group__in=groups, method='create')
    #     if not permissions:
    #         return Response({"message": "you don't have access to create a new component"})
    #     serialized_data = self.serializer_class(data=request.data)
    #     if serialized_data.is_valid():
    #         serialized_data.save()
    #         return Response(serialized_data.data, status=201)
    #     return Response(serialized_data.errors, status=400)

    # def retrieve(self, request, pk=None):
    #     user = request.user
    #     groups = user.groups.all()
    #     permissions = FieldPermission.objects.filter(group__in=groups, permission='see', instance_id=pk)
    #     if not permissions:
    #         return Response({"message": "You don't have access to see this particular component"})
    #     obj = self.get_object()
    #     fields = [permission.field for permission in permissions]
    #     serialized_data = {field: getattr(obj, field) for field in fields}
    #     return Response(serialized_data)

    # def destroy(self, request, pk=None):
    #     user = request.user
    #     groups = user.groups.all()
    #     permission = FieldPermission.objects.filter(group__in=groups, permission='')
    #     queryset = self.get_queryset()
    #     obj = self.get_object()
    #     obj.delete()
    #     return Response(status=204)


class FieldPermissionView(ModelViewSet):
    queryset = FieldPermission.objects.all()
    serializer_class = FieldPermissionSerializer
    permission_classes = [IsAuthenticated, IsGod, IsAdminUser]
