from django.contrib.auth.models import Group
from django.db import models

from ..core.models import BomBaseModel

fields = [
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

RUD = [
    "R_",
    "U_",
    "D_",
]  # CRUD without C

retrieve_update_delete = [
    "retrieve ",
    "update ",
    "delete ",
]

permission_codes = []
for method in RUD:
    for field in fields:
        permission_codes.append(method + field)
permission_codes.append("C")  # permission of creating a new component !!!

permission_names = []
for method in retrieve_update_delete:
    for field in fields:
        permission_names.append(method + field)
permission_names.append("create")


class BomComponent(BomBaseModel):
    revision = models.IntegerField(null=True, blank=True)
    ID = models.IntegerField(null=True, blank=True)
    P_on_N_status_code = models.IntegerField(null=True, blank=True)
    fig_no = models.CharField(max_length=16, null=True, blank=True)
    item_no = models.IntegerField(null=True, blank=True)
    module = models.CharField(max_length=16, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=32, null=True, blank=True)
    parent_code = models.CharField(max_length=32, null=True, blank=True)
    part_number = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=32, null=True, blank=True)
    comment = models.CharField(max_length=64, null=True, blank=True)
    sap_name = models.CharField(max_length=32, null=True, blank=True)
    unit_per_assy = models.IntegerField(null=True, blank=True)
    unit_per_end_item = models.IntegerField(null=True, blank=True)
    corrected_units_per_end_item = models.IntegerField(null=True, blank=True)
    gg_qty = models.IntegerField(null=True, blank=True)
    srp = models.CharField(max_length=32, null=True, blank=True)
    store_comment = models.TextField(max_length=1024, null=True, blank=True)
    assembly = models.BooleanField(default=False, null=True, blank=True)
    standard_part = models.BooleanField(default=False, null=True, blank=True)
    material = models.CharField(max_length=64, null=True, blank=True)
    mfg_complexity_level = models.CharField(max_length=64, null=True, blank=True)
    disassembled = models.CharField(
        max_length=64, null=True, blank=True
    )  # persian # moving the calendar from english to persian
    supplying_or_manufacturing = models.CharField(max_length=16, null=True, blank=True)
    internal_or_external_outsourcing = models.CharField(
        max_length=64, null=True, blank=True
    )
    vendor = models.CharField(max_length=64, null=True, blank=True)
    joining = models.CharField(max_length=64, null=True, blank=True)
    manufacturing_process = models.CharField(max_length=256, null=True, blank=True)
    raw_material_form = models.CharField(max_length=64, null=True, blank=True)
    function = models.CharField(max_length=64, null=True, blank=True)
    qc_criteria = models.CharField(max_length=32, null=True, blank=True)
    manufacturing_priority = models.CharField(max_length=64, null=True, blank=True)
    manufacturing_responsible_department = models.CharField(
        max_length=16, null=True, blank=True
    )  # relational to user groups
    designing_responsible_department = models.CharField(
        max_length=32, null=True, blank=True
    )
    usage_on_other_engines = models.CharField(max_length=64, null=True, blank=True)
    manufacturing_parts_category = models.CharField(
        max_length=64, null=True, blank=True
    )
    scope_matrix_category = models.CharField(max_length=64, null=True, blank=True)
    requires_manufacturing_or_supplying_for_reassembly = models.CharField(
        max_length=64, null=True, blank=True
    )
    system_D_requirements = models.TextField(max_length=1024, null=True, blank=True)
    percurment_state = models.CharField(max_length=64, null=True, blank=True)
    details = models.CharField(max_length=16, null=True, blank=True)
    joint_type = models.CharField(max_length=32, null=True, blank=True)
    discarded_during_disassembly = models.CharField(
        max_length=32, null=True, blank=True
    )
    expendables = models.BooleanField(null=True, blank=True)
    discarded_or_unusable_according_to_docs = models.CharField(
        max_length=32, null=True, blank=True
    )
    destroyed_for_analysis = models.CharField(max_length=32, null=True, blank=True)
    rejected_by_qc_or_inspection = models.CharField(
        max_length=32, null=True, blank=True
    )
    class_size_or_weight_as_required = models.CharField(
        max_length=32, null=True, blank=True
    )
    EBOM = models.IntegerField(null=True, blank=True)

    class Meta:
        permissions = list(zip(permission_codes, permission_names))


class FieldPermission(models.Model):
    instance_id = models.IntegerField(null=True, blank=True)
    FIELD_CHOISES = [
        ("revision", "revision"),
        ("ID", "ID"),
        ("P_on_N_status_code", "P_on_N_status_code"),
        ("fig_no", "fig_no"),
        ("item_no", "item_no"),
        ("module", "module"),
        ("level", "level"),
        ("code", "code"),
        ("parent_code", "parent_code"),
        ("part_number", "part_number"),
        ("description", "description"),
        ("comment", "comment"),
        ("sap_name", "sap_name"),
        ("unit_per_assy", "unit_per_assy"),
        ("unit_per_end_item", "unit_per_end_item"),
        ("corrected_units_per_end_item", "corrected_units_per_end_item"),
        ("gg_qty", "gg_qty"),
        ("srp", "srp"),
        ("store_comment", "store_comment"),
        ("assembly", "assembly"),
        ("standard_part", "standard_part"),
        ("material", "material"),
        ("mfg_complexity_level", "mfg_complexity_level"),
        ("disassembled", "disassembled"),
        ("supplying_or_manufacturing", "supplying_or_manufacturing"),
        ("internal_or_external_outsourcing", "internal_or_external_outsourcing"),
        ("vendor", "vendor"),
        ("joining", "joining"),
        ("manufacturing_process", "manufacturing_process"),
        ("raw_material_form", "raw_material_form"),
        ("function", "function"),
        ("qc_criteria", "qc_criteria"),
        ("manufacturing_priority", "manufacturing_priority"),
        (
            "manufacturing_responsible_department",
            "manufacturing_responsible_department",
        ),
        ("designing_responsible_department", "designing_responsible_department"),
        ("usage_on_other_engines", "usage_on_other_engines"),
        ("manufacturing_parts_category", "manufacturing_parts_category"),
        ("scope_matrix_category", "scope_matrix_category"),
        (
            "requires_manufacturing_or_supplying_for_reassembly",
            "requires_manufacturing_or_supplying_for_reassembly",
        ),
        ("system_D_requirements", "system_D_requirements"),
        ("percurment_state", "percurment_state"),
        ("details", "details"),
        ("joint_type", "joint_type"),
        ("discarded_during_disassembly", "discarded_during_disassembly"),
        ("expendables", "expendables"),
        (
            "discarded_or_unusable_according_to_docs",
            "discarded_or_unusable_according_to_docs",
        ),
        ("destroyed_for_analysis", "destroyed_for_analysis"),
        ("rejected_by_qc_or_inspection", "rejected_by_qc_or_inspection"),
        ("class_size_or_weight_as_required", "class_size_or_weight_as_required"),
        ("EBOM", "EBOM"),
    ]
    field = models.CharField(
        max_length=128, null=True, blank=True, choices=FIELD_CHOISES
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    editable = models.BooleanField()

    def __str__(self):
        return f"{self.editable} {self.instance_id} {self.field}"
