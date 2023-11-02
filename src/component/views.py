import json
import re

from django.contrib.auth.models import Group
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.http import QueryDict
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
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
    ScopeMatrix,
    ScopeMatrixFieldPermission,
)
from .serializers import (
    BomComponentSerializer,
    BomFieldPermissionSerializer,
    DesignSerializer,
    LateralSerializer,
    ManufacturingSerializer,
    MassPermissionSerializer,
    ProvideComponentSerializer,
    ProvideFieldPermissionSerializer,
    ScopeMatrixComponentSerializer,
    ScopeMatrixFieldPermissionSerializer,
    TwentyEightDevicesManufacturingSerializer,
    TwentyEightDevicesQualitySerializer,
    TwentyEightDevicesSideSerializer,
    TwoDevicesManufacturingSerializer,
    TwoDevicesQualitySerializer,
    TwoDevicesSideSerializer,
    originalCoreSerializer,
)

# PAGINATION_CLASSES = {
#     'cursor': CursorPagination,
#     'page_number': CustomPageNumberPagination,
# }

correct_kwargs = [
    "bom",
    "provide",
    "scope",
    "core",
    "design",
    "lateral",
    "manufacturing",
    "2-devices-side",
    "28-devices-side",
    "2-devices-manufacturing",
    "28-devices-manufacturing",
    "2-devices-quality",
    "28-devices-quality",
]

scope_kwargs = [
    "scope",
    "core",
    "design",
    "lateral",
    "manufacturing",
    "2-devices-side",
    "28-devices-side",
    "2-devices-manufacturing",
    "28-devices-manufacturing",
    "2-devices-quality",
    "28-devices-quality",
]


class InvalidTableException(APIException):
    status_code = 404
    default_detail = "Invalid table specified."
    default_code = "invalid_table"


def check_invalid_engine(engine):
    if engine not in correct_kwargs:
        raise InvalidTableException()


def find_permission_model(kwargs):
    check_invalid_engine(kwargs)
    if kwargs == "bom":
        return BomFieldPermission.objects.all()
    elif kwargs == "provide":
        return ProvideFieldPermission.objects.all()
    elif kwargs == "scope":
        return ScopeMatrixFieldPermission.objects.all()


def find_component_model(kwargs):
    check_invalid_engine(kwargs)
    if kwargs == "bom":
        return BomComponent.objects.all()
    elif kwargs == "provide":
        return ProvideComponent.objects.all()
    elif kwargs in scope_kwargs:
        return ScopeMatrix.objects.all()


def find_permission_serializer(kwargs):
    check_invalid_engine(kwargs)
    if kwargs == "bom":
        return BomFieldPermissionSerializer
    elif kwargs == "provide":
        return ProvideFieldPermissionSerializer
    elif kwargs == "scope":
        return ScopeMatrixFieldPermissionSerializer


def find_component_serializer(kwargs):
    check_invalid_engine(kwargs)
    if kwargs == "bom":
        return BomComponentSerializer
    elif kwargs == "provide":
        return ProvideComponentSerializer
    elif kwargs == "core":
        return originalCoreSerializer
    elif kwargs == "design":
        return DesignSerializer
    elif kwargs == "lateral":
        return LateralSerializer
    elif kwargs == "manufacturing":
        return ManufacturingSerializer
    elif kwargs == "2-devices-side":
        return TwoDevicesSideSerializer
    elif kwargs == "28-devices-side":
        return TwentyEightDevicesSideSerializer
    elif kwargs == "2-devices-manufacturing":
        return TwoDevicesManufacturingSerializer
    elif kwargs == "28-devices-manufacturing":
        return TwentyEightDevicesManufacturingSerializer
    elif kwargs == "2-devices-quality":
        return TwoDevicesQualitySerializer
    elif kwargs == "28-devices-quality":
        return TwentyEightDevicesQualitySerializer


class Component(ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination
    scope_fields_to_return = []

    common_fields = [
        "id",
        "original_report_id",
        "fig_no",
        "item_no",
        "module",
        "TUGA_subtitute_part_number",
        "old_system_part_no",
        "description",
        "unit_per_end_item",
        "assembly",
        "standard_part",
        "new_manufacturing_responsible_department",
        "level",
    ]

    def scope_fields_to_return_func(self):
        if self.kwargs["table"] == "bom":
            self.scope_fields_to_return = [
                "id",
                "revision",
                "ID",
                "P_on_N_status_code",
                "fig_no",
                "item_no",
                "module",
                "level",
                "code",
                "parent_code",
                "part_number",
                "description",
                "comment",
                "sap_name",
                "unit_per_assy",
                "unit_per_end_item",
                "corrected_units_per_end_item",
                "gg_qty",
                "srp",
                "store_comment",
                "assembly",
                "standard_part",
                "material",
                "mfg_complexity_level",
                "disassembled",
                "supplying_or_manufacturing",
                "internal_or_external_outsourcing",
                "vendor",
                "joining",
                "manufacturing_process",
                "raw_material_form",
                "function",
                "qc_criteria",
                "manufacturing_priority",
                "manufacturing_responsible_department",
                "designing_responsible_department",
                "usage_on_other_engines",
                "manufacturing_parts_category",
                "scope_matrix_category",
                "requires_manufacturing_or_supplying_for_reassembly",
                "system_D_requirements",
                "percurment_state",
                "details",
                "joint_type",
                "discarded_during_disassembly",
                "expendables",
                "discarded_or_unusable_according_to_docs",
                "destroyed_for_analysis",
                "rejected_by_qc_or_inspection",
                "class_size_or_weight_as_required",
                "EBOM",
            ]
        if self.kwargs["table"] == "provide":
            self.scope_fields_to_return = [
                "id",
                "application_type",
                "supply_stage",
                "material_supplier",
                "pr",
                "po",
                "subject",
                "request_type",
                "customer_management",
                "contract_number",
                "supplier",
                "amount",
                "adjustment_amount",
                "currency",
                "expert",
                "prepayment_percentage",
                "currency_type",
                "prepayment_according_to_contract",
                "prepaid_by_toga",
                "prepaid_by_air_engine",
                "prepayment_guarantee_check",
                "prepayment_guarantee",
                "mortgage_document_guarantee",
                "financial_situation",
                "prepayment_request_date",
                "prepayment_amount",
                "prepayment_date",
            ]
        elif self.kwargs["table"] == "core":
            self.scope_fields_to_return = self.common_fields + [
                "disassembled",
                "progress_certificate",
                "ThreeD_scan_progress",
                "ThreeD_scan_certificate",
                "Fi_100_percent_l_modelling",
                "Fi_100_percent_l_modelling_certificate",
                "level_2_drawing",
                "level_2_drawing_certificate",
                "level_3_drawing",
                "level_3_drawing_certificate",
                "assembly_drawing",
                "construction_plan_with_assembly_view",
                "identification_report_metallurgical_notebook_of_the_piece",
                "certificate_code",
                "identification_report_metallurgical_notebook_of_the_piece_certi",
                "raw_material_spec",
                "raw_material_spec_certificate",
                "part_spec",
                "part_spec_certificate",
                "cover_spec",
                "cover_spec_certificate",
                "connections_spec",
                "connections_spec_certificate",
                "other_specs_complementary_operations",
                "other_specs_certificate",
                "interprocess_maps",
                "interprocess_maps_certificate",
                "OPC_or_MPP_rating",
                "rating_certificate",
                "TP",
                "TP_certificate",
                "MQCP",
                "MQCP_certificate",
                "ITP",
                "ITP_certificate",
                "contract",
                "_2_manufacturing_total_progress",
                "_28_manufacturing_total_progress",
                "_2_quality_total_progress",
                "_28_quality_total_progress",
            ]
        elif self.kwargs["table"] == "design":
            self.scope_fields_to_return = self.common_fields + [
                "disassembled",
                "progress_certificate",
                "ThreeD_scan_progress",
                "ThreeD_scan_certificate",
                "Fi_100_percent_l_modelling",
                "Fi_100_percent_l_modelling_certificate",
                "level_2_drawing",
                "level_2_drawing_certificate",
                "level_3_drawing",
                "level_3_drawing_certificate",
                "assembly_drawing",
                "construction_plan_with_assembly_view",
                "certificate_code",
            ]
        elif self.kwargs["table"] == "lateral":
            self.scope_fields_to_return = self.common_fields + [
                "disassembled",
                "progress_certificate",
                "ThreeD_scan_progress",
                "ThreeD_scan_certificate",
                "Fi_100_percent_l_modelling",
                "Fi_100_percent_l_modelling_certificate",
                "level_2_drawing",
                "level_2_drawing_certificate",
                "level_3_drawing",
                "level_3_drawing_certificate",
                "assembly_drawing",
                "construction_plan_with_assembly_view",
                "certificate_code",
                "identification_report_metallurgical_notebook_of_the_piece",
                "identification_report_metallurgical_notebook_of_the_piece_certi",
                "raw_material_spec",
                "raw_material_spec_certificate",
                "part_spec",
                "part_spec_certificate",
                "cover_spec",
                "cover_spec_certificate",
                "connections_spec",
                "connections_spec_certificate",
                "other_specs_complementary_operations",
                "other_specs_certificate",
                "interprocess_maps",
                "interprocess_maps_certificate",
                "OPC_or_MPP_rating",
                "rating_certificate",
                "TP",
                "TP_certificate",
                "MQCP",
                "MQCP_certificate",
                "ITP",
                "ITP_certificate",
            ]
        elif self.kwargs["table"] == "manufacturing":
            self.scope_fields_to_return = self.common_fields + [
                "identification_report_metallurgical_notebook_of_the_piece",
                "identification_report_metallurgical_notebook_of_the_piece_certi",
                "raw_material_spec",
                "raw_material_spec_certificate",
                "part_spec",
                "part_spec_certificate",
                "cover_spec",
                "cover_spec_certificate",
                "connections_spec",
                "connections_spec_certificate",
                "other_specs_complementary_operations",
                "other_specs_certificate",
                "interprocess_maps",
                "interprocess_maps_certificate",
                "OPC_or_MPP_rating",
                "rating_certificate",
                "TP",
                "TP_certificate",
                "MQCP",
                "MQCP_certificate",
                "ITP",
                "ITP_certificate",
            ]
        elif self.kwargs["table"] == "2-devices-side":
            self.scope_fields_to_return = self.common_fields + [
                "_3885",
                "contract",
                "adv_payment",
                "material_supply",
                "mold_or_die_or_fixture",
                "casting",
                "forge",
                "forming",
                "machining",
                "brazing_or_welding",
                "coating",
                "dummy_sample",
                "first_articles",
                "first_articles_test",
                "_2_side_total_progress",
            ]
        elif self.kwargs["table"] == "28-devices-side":
            self.scope_fields_to_return = self.common_fields + [
                "_3885",
                "contract",
                "adv_payment",
                "material_supply",
                "mold_or_die_or_fixture",
                "casting",
                "forge",
                "forming",
                "machining",
                "brazing_or_welding",
                "coating",
                "mass_production",
                "_28_side_total_progress",
            ]
        elif self.kwargs["table"] == "2-devices-manufacturing":
            self.scope_fields_to_return = self.common_fields + [
                "_3885",
                "contract",
                "adv_payment",
                "material_supply",
                "mold_or_die_or_fixture",
                "casting",
                "forge",
                "forming",
                "machining",
                "brazing_or_welding",
                "coating",
                "dummy_sample",
                "first_articles",
                "first_articles_test",
                "_2_manufacturing_total_progress",
            ]
        elif self.kwargs["table"] == "28-devices-manufacturing":
            self.scope_fields_to_return = self.common_fields + [
                "_3885",
                "contract",
                "adv_payment",
                "material_supply",
                "mold_or_die_or_fixture",
                "casting",
                "forge",
                "forming",
                "machining",
                "brazing_or_welding",
                "coating",
                "mass_production",
                "_28_manufacturing_total_progress",
            ]
        elif self.kwargs["table"] == "2-devices-quality":
            self.scope_fields_to_return = self.common_fields + [
                "review_and_ITP_approval_4_percent",
                "qualitative_evaluation_the_contractor_2_percent",
                "kick_off_meeting_3_percent",
                "CDR_5_percent",
                "compliant_quality_inspection_ITP_or_MQCP_65_percent",
                "submitting_an_inspection_report_accept_or_NCR_7_percent",
                "check_the_answer_design_to_NCR_5_percent",
                "issuing_quality_tag_2_percent",
                "compilation_and_approval_final_book_5_percent",
                "issuance_of_test_certificate_or_Form1_or_CoC_2_percent",
                "_2_quality_total_progress",
            ]
        elif self.kwargs["table"] == "28-devices-quality":
            self.scope_fields_to_return = self.common_fields + [
                "compliant_quality_inspection_ITP_or_MQCP_75_percent",
                "submitting_an_inspection_report_accept_or_NCR_12_percent",
                "check_the_answer_design_to_NCR_3_percent",
                "issuing_quality_tag_2_percent",
                "compilation_and_approval_final_book_6_percent",
                "issuance_of_test_certificate_or_Form1_or_CoC_2_percent",
                "_28_quality_total_progress",
            ]

    def get_queryset(self):
        return find_component_model(self.kwargs["table"])

    def get_serializer_class(self):
        return find_component_serializer(self.kwargs["table"])

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

        self.scope_fields_to_return_func()
        fields_to_return = self.scope_fields_to_return
        instances = instances.filter(
            instance_id__in=instance_ids, field__in=fields_to_return
        )
        raw_queryset = self.get_queryset()
        queryset = raw_queryset.filter(id__in=instance_ids).values(*fields_to_return)

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
                queryset_dict[id][field] = obj[field] if field != None else None
                # queryset_dict[id][field] = getattr(obj, field) if field != None else None
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
        return find_permission_model(self.kwargs["table"])

    def get_serializer_class(self):
        return find_permission_serializer(self.kwargs["table"])

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
        component = find_component_model(self.kwargs["table"])

        initial_list = [{'id': i} for i in range(1, component.count()+1)]

        for instance in instances:
            id = instance.instance_id
            try:
                if id not in editable_dict:
                    editable_dict[id] = {"id": id}
                editable_dict[id][instance.field] = instance.editable
            except:
                pass
        
        editable_values = list(editable_dict.values())
        editable_values += [item for item in initial_list if not any(item['id'] == i['id'] for i in editable_values)]
        response_data = {
            "editables": editable_values,
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
    permission_classes = [IsAuthenticated, IsGod, IsAdminUser]

    def get_queryset(self):
        return find_permission_model(self.kwargs["table"])

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
            instances = [
                queryset.model(
                    instance_id=instance_id, field=field, group=group, editable=editable
                )
                for instance_id in range(1, count + 1)
            ]
            queryset.bulk_create(instances)
        return Response({"message": "Done"})
