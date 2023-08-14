import json
import re

from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..core.paginations import CustomCursorPagination, CustomPageNumberPagination
from ..core.permissions import IsGod
from ..core.versatile_funcs import compare_instance_with_dict
from .models import BomComponent, FieldPermission
from .serializers import ComponentSerializer, FieldPermissionSerializer

# PAGINATION_CLASSES = {
#     'cursor': CursorPagination,
#     'page_number': CustomPageNumberPagination,
# }


class Component(ModelViewSet):
    queryset = BomComponent.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

    """
        page number pagination
    """

    def list(self, request, *args, **kwargs):
        user = self.request.user
        groups = user.groups.all()
        page = (
            re.findall(r"\d+", request.query_params.get("page"))
            if request.query_params.get("page")
            else ""
        )
        page = int(page[0]) if page else 0

        instances = FieldPermission.objects.filter(group__in=groups).order_by(
            "instance_id"
        )
        paginator = Paginator(
            instances.values_list("instance_id", flat=True).distinct(), 15
        )
        instance_ids = paginator.get_page(page)
        instances = instances.filter(instance_id__in=instance_ids)

        queryset = self.queryset.filter(id__in=instance_ids)
        queryset_dict = {}
        editable_dict = {}
        for instance in instances:
            id = instance.instance_id
            field = instance.field
            editable = instance.editable
            try:
                if id not in queryset_dict:
                    obj = queryset.get(id=id)
                    queryset_dict[id] = {"id": id}
                    editable_dict[id] = {"id": id}
                queryset_dict[id][field] = getattr(obj, field)
                editable_dict[id][field] = editable
            except BomComponent.DoesNotExist:
                pass

        response_data = {
            "querysets": list(queryset_dict.values()),
            "editables": list(editable_dict.values()),
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
    #             obj = queryset.get(id=id)
    #             field = instance.field
    #             field_value = getattr(obj, field)
    #             try:
    #                 if id not in queryset_dict:
    #                     queryset_dict[id] = {
    #                         "id": id,
    #                     }
    #                 queryset_dict[id][field] = field_value
    #             except BomComponent.DoesNotExist:
    #                 pass

    #         return self.get_paginated_response(list(queryset_dict.values()))

    #     return Response([], status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        obj = BomComponent.objects.get(id=pk)
        initial_obj = obj
        json_dict = request.data
        instances = FieldPermission.objects.filter(
            group__in=groups, editable=True, instance_id=pk
        )
        notEditable_instances = FieldPermission.objects.filter(
            group__in=groups, editable=False, instance_id=pk
        )
        if not instances:
            return Response({"message": "anyAccess"})

        try:
            for instance in instances:
                for key, value in json_dict.items():
                    if instance.field == key and instance.editable:
                        data = {f"{key}": value}
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
                        obj = BomComponent.objects.get(id=pk)
                        queryset_dict[id] = {"id": id}
                    queryset_dict[id][field_name] = getattr(obj, field_name)
                except BomComponent.DoesNotExist:
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
                    obj = BomComponent.objects.get(id=pk)
                    queryset_dict[id] = {"id": id}
                queryset_dict[id][field_name] = getattr(obj, field_name)
            except BomComponent.DoesNotExist:
                pass
        queryset_list = list(queryset_dict.values())
        updated_keys = [
            key
            for key, value in request.data.items()
            for key_2, value_2 in initial_obj.__dict__.items()
            if key == key_2 and value_2 != value
        ]
        # print(f'updated_keys : {notEditable_instances}')

        result = any(
            updated_key != editable.field
            for editable in instances
            for updated_key in updated_keys
        )

        true_response = {
            "message": "permission" if result else "success",
            "data": queryset_list,
        }
        return Response(true_response, status=status.HTTP_200_OK)


class FieldPermissionView(ModelViewSet):
    queryset = FieldPermission.objects.all()
    serializer_class = FieldPermissionSerializer
    permission_classes = [IsAuthenticated, IsGod, IsAdminUser]
    # lookup_field = 'group'
    # pagination_class = CustomPageNumberPagination

    # def get_queryset(self):
    #     print(f'groups : {self.kwargs["group"]}')
    #     return self.queryset.filter(group=self.kwargs["group"])

    def list(self, request, *args, **kwargs):
        # print(f'groups : {request.query_params.get("group")}')
        group = request.query_params.get("group")

        user = self.request.user
        groups = user.groups.all()
        page = (
            re.findall(r"\d+", request.query_params.get("page"))
            if request.query_params.get("page")
            else ""
        )
        page = int(page[0]) if page else 0
        print(f"request.data : {request.data}")

        instances = self.queryset.filter(group__name=group).order_by("instance_id")
        paginator = Paginator(
            instances.values_list("instance_id", flat=True).distinct(), 15
        )
        instance_ids = paginator.get_page(page)
        instances = instances.filter(instance_id__in=instance_ids)

        editable_dict = {}
        for instance in instances:
            id = instance.instance_id
            field = instance.field
            editable = instance.editable
            try:
                if id not in editable_dict:
                    editable_dict[id] = {"id": id}
                editable_dict[id][field] = editable
            except BomComponent.DoesNotExist:
                pass

        return Response(list(editable_dict.values()), status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        obj = BomComponent.objects.get(id=pk)
        initial_obj = obj
        json_dict = request.data
        print(f"json_dict : {json_dict}")
        instances = self.queryset.filter(
            group__in=groups, editable=True, instance_id=pk
        )
        notEditable_instances = self.queryset.filter(
            group__in=groups, editable=False, instance_id=pk
        )
        if not instances:
            return Response({"message": "anyAccess"})

        try:
            for instance in instances:
                for key, value in json_dict.items():
                    if instance.field == key and instance.editable:
                        data = {f"{key}": value}
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
                        obj = BomComponent.objects.get(id=pk)
                        queryset_dict[id] = {"id": id}
                    queryset_dict[id][field_name] = getattr(obj, field_name)
                except BomComponent.DoesNotExist:
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
                    obj = BomComponent.objects.get(id=pk)
                    queryset_dict[id] = {"id": id}
                queryset_dict[id][field_name] = getattr(obj, field_name)
            except BomComponent.DoesNotExist:
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

        true_response = {
            "message": "permission" if result else "success",
            "data": queryset_list,
        }
        return Response(true_response, status=status.HTTP_200_OK)
