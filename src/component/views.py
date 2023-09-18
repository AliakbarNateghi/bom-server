import json
import re

from django.contrib.auth.models import Group
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from ..core.paginations import CustomCursorPagination, CustomPageNumberPagination
from ..core.permissions import IsGod
from ..core.versatile_funcs import compare_instance_with_dict
from ..user.models import Department
from .models import (
    BomComponent,
    BomFieldPermission,
    ProvideComponent,
    ProvideFieldPermission,
)
from .serializers import (
    BomComponentSerializer,
    BomFieldPermissionSerializer,
    MassPermissionSerializer,
    ProvideComponentSerializer,
    ProvideFieldPermissionSerializer,
)

# PAGINATION_CLASSES = {
#     'cursor': CursorPagination,
#     'page_number': CustomPageNumberPagination,
# }


def find_permission_model(kwargs):
    if kwargs == "bom":
        return BomFieldPermission.objects.all()
    elif kwargs == "provide":
        return ProvideFieldPermission.objects.all()


def find_component_model(kwargs):
    if kwargs == "bom":
        return BomComponent.objects.all()
    elif kwargs == "provide":
        return ProvideComponent.objects.all()


class Component(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        if self.kwargs["table"] == "bom":
            return BomComponent.objects.all()
        elif self.kwargs["table"] == "provide":
            return ProvideComponent.objects.all()

    def get_serializer_class(self):
        if self.kwargs["table"] == "bom":
            return BomComponentSerializer
        elif self.kwargs["table"] == "provide":
            return ProvideComponentSerializer

    """
        page number pagination
    """

    def list(self, request, *args, **kwargs):
        permission_model = find_permission_model(self.kwargs["table"])
        user = self.request.user
        groups = user.groups.all()
        page = (
            re.findall(r"\d+", request.query_params.get("page"))
            if request.query_params.get("page")
            else ""
        )
        page = int(page[0]) if page else 0

        instances = permission_model.filter(group__in=groups).order_by("instance_id")
        paginator = Paginator(
            instances.values_list("instance_id", flat=True).distinct(), 100
        )
        instance_ids = paginator.get_page(page)
        instances = instances.filter(instance_id__in=instance_ids)
        raw_queryset = self.get_queryset()
        queryset = raw_queryset.filter(id__in=instance_ids)
        queryset_dict = {}
        editable_dict = {}
        count = 0
        for instance in instances:
            id = instance.instance_id
            field = instance.field
            count += 1
            editable = instance.editable
            try:
                if id not in queryset_dict:
                    obj = queryset.get(id=id)
                    queryset_dict[id] = {"id": id}
                    editable_dict[id] = {"id": id}
                # queryset_dict[id][field] = json.loads(serializers.serialize('json', [getattr(obj, field), ]))[0]["fields"]["name"] if type(getattr(obj, field)) == Department else getattr(obj, field)
                queryset_dict[id][field] = getattr(obj, field) if field != None else None              
                editable_dict[id][field] = editable
            except queryset.model.DoesNotExist:
                pass

        response_data = {
            "querysets": list(queryset_dict.values()),
            "editables": list(editable_dict.values()),
            "count": raw_queryset.count(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    """
        cursor pagination
    """
    # def list(self, request, *args, **kwargs):
    #     user = request.user
    #     groups = user.groups.all()
    #     instances = self.paginate_queryset(
    #         FieldPermission.objects.filter(group__in=groups).order_by("instance_id")
    #     )
    #     instance_ids = list(set([instance.instance_id for instance in instances]))

    #     queryset = self.queryset.filter(id__in=instance_ids)
    #     if instance_ids is not None:
    #         queryset_dict = {}
    #         for instance in instances:
    #             id = instance.instance_id
    #             field = instance.field
    #             try:
    #                 if id not in queryset_dict:
    #                     obj = queryset.get(id=id)
    #                     queryset_dict[id] = {
    #                         "id": id,
    #                     }
    #                 queryset_dict[id][field] = getattr(obj, field)
    #             except BomComponent.DoesNotExist:
    #                 pass

    #         return self.get_paginated_response(list(queryset_dict.values()))

    #     return Response([], status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None, **kwargs):
        permission_model = find_permission_model(self.kwargs["table"])
        user = request.user
        groups = user.groups.all()
        queryset = self.get_queryset()
        obj = queryset.get(id=pk)
        initial_obj = obj
        json_dict = request.data
        instances = permission_model.filter(
            group__in=groups, editable=True, instance_id=pk
        )
        notEditable_instances = permission_model.filter(
            group__in=groups, editable=False, instance_id=pk
        )
        if not instances:
            return Response({"message": "anyAccess"})

        try:
            for instance in instances:
                if instance.field in json_dict and instance.editable:
                    value = json_dict[instance.field]
                    # for instance in instances:
                    #     for key, value in json_dict.items():
                    # print(f"key : {key}")
                    print(f"instance.field : {instance.field}")
                    #         if instance.field == key and instance.editable:
                    data = {f"{instance.field}": value}
                    serializer = self.get_serializer(obj, data=data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
        except:
            queryset_dict = {}
            for instance in instances:
                field_name = instance.field
                id = instance.instance_id
                try:
                    if id not in queryset_dict:
                        obj = queryset.get(id=pk)
                        queryset_dict[id] = {"id": id}
                    queryset_dict[id][field_name] = getattr(obj, field_name)
                except queryset.model.DoesNotExist:
                    pass
            queryset_list = list(queryset_dict.values())
            false_type_response = {"message": "type", "data": queryset_list}
            return Response(false_type_response, status=status.HTTP_200_OK)
        queryset_dict = {}
        for instance in instances:
            field_name = instance.field
            id = instance.instance_id
            try:
                if id not in queryset_dict:
                    obj = queryset.get(id=pk)
                    queryset_dict[id] = {"id": id}
                queryset_dict[id][field_name] = getattr(obj, field_name)
            except queryset.model.DoesNotExist:
                pass
        queryset_list = list(queryset_dict.values())
        updated_keys = [
            key
            for key, value in request.data.items()
            for key_2, value_2 in initial_obj.__dict__.items()
            if key == key_2 and value_2 != value
        ]

        result = any(
            updated_key == not_editable.field
            for not_editable in notEditable_instances
            for updated_key in updated_keys
        )
        # or any(
        #     updated_key != not_editable.field and updated_key != instance.field
        #     for instance in instances
        #     for not_editable in notEditable_instances
        #     for updated_key in updated_keys
        # )

        true_response = {
            "message": "permission" if result else "success",
            "data": queryset_list,
        }
        return Response(true_response, status=status.HTTP_200_OK)


class FieldPermissionView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsGod, IsAdminUser]

    def get_queryset(self):
        if self.kwargs["table"] == "bom":
            return BomFieldPermission.objects.all()
        elif self.kwargs["table"] == "provide":
            return ProvideFieldPermission.objects.all()

    def get_serializer_class(self):
        if self.kwargs["table"] == "bom":
            print
            return BomFieldPermissionSerializer
        elif self.kwargs["table"] == "provide":
            return ProvideFieldPermissionSerializer

    def list(self, request, *args, **kwargs):
        group = (
            re.findall(r"\d+", request.query_params.get("group"))
            if request.query_params.get("group")
            else ""
        )
        group = int(group[0]) if group else 0

        page = (
            re.findall(r"\d+", request.query_params.get("page"))
            if request.query_params.get("page")
            else ""
        )
        page = int(page[0]) if page else 0
        queryset = self.get_queryset()
        instances = queryset.filter(group__id=group).order_by("instance_id")
        paginator = Paginator(
            instances.values_list("instance_id", flat=True).distinct(), 100
        )
        instance_ids = paginator.get_page(page)
        instances = instances.filter(instance_id__in=instance_ids)

        editable_dict = {}
        for instance in instances:
            id = instance.instance_id
            try:
                if id not in editable_dict:
                    editable_dict[id] = {"id": id}
                editable_dict[id][instance.field] = instance.editable
            except:
                pass

        component = find_component_model(self.kwargs["table"])
        response_data = {
            "editables": list(editable_dict.values()),
            "count": component.count(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        queryset = self.get_queryset()
        permissions = queryset.filter(instance_id=self.instance_id, group=self.group)
        editable_dict = {}
        for instance in permissions:
            id = instance.instance_id
            field = instance.field
            editable = instance.editable
            try:
                if id not in editable_dict:
                    editable_dict[id] = {"id": id}
                editable_dict[id][field] = editable
            except:
                pass

        return Response(list(editable_dict.values()), status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        self.group = serializer.validated_data.get("group")
        self.field = serializer.validated_data.get("field")
        self.instance_id = serializer.validated_data.get("instance_id")
        queryset = self.get_queryset()
        instance = queryset.filter(
            group=self.group,
            field=self.field,
            instance_id=self.instance_id,
        ).first()
        if instance:
            instance.delete()
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance_id = kwargs["pk"]
        field = request.GET.get("field")
        group = request.GET.get("group")
        queryset = self.get_queryset()
        instance = queryset.filter(
            group__id=group,
            instance_id=instance_id,
            field=field,
        ).first()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MassPermissionViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    serializer_class = MassPermissionSerializer

    def get_queryset(self):
        if self.kwargs["table"] == "bom":
            return BomFieldPermission.objects.all()
        elif self.kwargs["table"] == "provide":
            return ProvideFieldPermission.objects.all()

    # def get_serializer_class(self):
    #     if self.kwargs['table'] == 'bom':
    #         return BomComponentSerializer
    #     elif self.kwargs['table'] == 'provide':
    #         return ProvideComponentSerializer
    permission_classes = [IsAuthenticated, IsGod, IsAdminUser]

    def create(self, request, *args, **kwargs):
        component = find_component_model(self.kwargs["table"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        field = serializer.validated_data["field"]
        group = serializer.validated_data["group"]
        editable = serializer.validated_data.get("editable")
        queryset = self.get_queryset()
        queryset.filter(field=field, group=group).delete()
        if editable != None:
            group = Group.objects.get(id=group)
            count = component.count()
            print(count)
            instances = [
                queryset.model(
                    instance_id=instance_id, field=field, group=group, editable=editable
                )
                for instance_id in range(1, count + 1)
            ]
            queryset.bulk_create(instances)
        return Response({"message": "Done"})
