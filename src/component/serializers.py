from rest_framework import serializers

from .models import (
    BomComponent,
    BomFieldPermission,
    ProvideComponent,
    ProvideFieldPermission,
    ScopeMatrix,
    ScopeMatrixFieldPermission,
)


class BomComponentSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = BomComponent
        # fields = "__all__"
        exclude = [
            # 'id',
            "deleted",
            "deletable",
            # 'editable',
        ]


class ProvideComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvideComponent
        exclude = [
            # 'id',
            "deleted",
            "deletable",
            # 'editable',
        ]


common_fields = [
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


class ScopeMatrixComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = [
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
            "mass_production",
            "_2_manufacturing_total_progress",
            "_28_manufacturing_total_progress",
            "_2_side_total_progress",
            "_28_side_total_progress",
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
            "compliant_quality_inspection_ITP_or_MQCP_75_percent",
            "submitting_an_inspection_report_accept_or_NCR_12_percent",
            "check_the_answer_design_to_NCR_3_percent",
            "issuing_quality_tag_2_percent",
            "compilation_and_approval_final_book_6_percent",
            "issuance_of_test_certificate_or_Form1_or_CoC_2_percent",
            "_28_quality_total_progress",
        ]


class originalCoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class LateralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class ManufacturingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class TwoDevicesSideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class TwentyEightDevicesSideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class TwoDevicesManufacturingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class TwentyEightDevicesManufacturingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class TwoDevicesQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
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


class TwentyEightDevicesQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrix
        fields = common_fields + [
            "compliant_quality_inspection_ITP_or_MQCP_75_percent",
            "submitting_an_inspection_report_accept_or_NCR_12_percent",
            "check_the_answer_design_to_NCR_3_percent",
            "issuing_quality_tag_2_percent",
            "compilation_and_approval_final_book_6_percent",
            "issuance_of_test_certificate_or_Form1_or_CoC_2_percent",
            "_28_quality_total_progress",
        ]


class BomFieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomFieldPermission
        fields = ["group", "field", "instance_id", "editable"]


class ProvideFieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvideFieldPermission
        fields = ["group", "field", "instance_id", "editable"]


class ScopeMatrixFieldPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeMatrixFieldPermission
        fields = ["group", "field", "instance_id", "editable"]


class MassPermissionSerializer(serializers.Serializer):
    field = serializers.CharField(required=True)
    group = serializers.IntegerField(required=True)
    editable = serializers.BooleanField(required=False, allow_null=True)
