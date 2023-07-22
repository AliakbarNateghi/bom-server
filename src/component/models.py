from django.db import models
from django.contrib.auth.models import Group

from ..core.models import BomBaseModel

fields = [
    'revision',
    'ID',
    'P_on_N_status_code',
    'fig_no',
    'item_no',
    'module',
    'level',
    'code',
    'parent_code',
    'part_number',
    'description',
    'comment',
    'sap_name',
    'unit_per_assy',
    'unit_per_end_item',
    'corrected_units_per_end_item',
    'gg_qty',
    'srp',
    'store_comment',
    'assembly',
    'standard_part',
    'material',
    'mfg_complexity_level',
    'disassembled',
    'supplying_or_manufacturing',
    'internal_or_external_outsourcing',
    'vendor',
    'joining',
    'manufacturing_process',
    'raw_material_form',
    'function',
    'qc_criteria',
    'manufacturing_priority',
    'manufacturing_responsible_department',
    'designing_responsible_department',
    'usage_on_other_engines',
    'manufacturing_parts_category',
    'scope_matrix_category',
    'requires_manufacturing_or_supplying_for_reassembly',
    'system_D_requirements',
    'percurment_state',
    'details',
    'joint_type',
    'discarded_during_disassembly',
    'expendables',
    'discarded_or_unusable_according_to_docs',
    'destroyed_for_analysis',
    'rejected_by_qc_or_inspection',
    'class_size_or_weight_as_required',
    'EBOM',
]

RUD = ['R_', 'U_', 'D_',] # CRUD without C

retrieve_update_delete = ['retrieve ', 'update ', 'delete ',]

permission_codes = []
for method in RUD:
    for field in fields:
        permission_codes.append(method + field)
permission_codes.append("C") # permission of creating a new component !!!

permission_names = []
for method in retrieve_update_delete:
    for field in fields:
        permission_names.append(method + field)
permission_names.append("create")

class BomComponent(BomBaseModel):
    revision = models.IntegerField()
    ID = models.IntegerField()
    P_on_N_status_code = models.IntegerField()
    fig_no = models.CharField(max_length=16)
    item_no = models.IntegerField()
    module = models.CharField(max_length=16)
    level = models.IntegerField()
    code = models.CharField(max_length=32)
    parent_code = models.CharField(max_length=32)
    part_number = models.CharField(max_length=128)
    description = models.CharField(max_length=32)
    comment = models.CharField(max_length=64)
    sap_name = models.CharField(max_length=32)
    unit_per_assy = models.IntegerField()
    unit_per_end_item = models.IntegerField()
    corrected_units_per_end_item = models.IntegerField()
    gg_qty = models.IntegerField()
    srp = models.CharField(max_length=32) 
    store_comment = models.TextField(max_length=1024)
    assembly = models.BooleanField(default=False)
    standard_part = models.BooleanField(default=False)
    material = models.CharField(max_length=64)
    mfg_complexity_level = models.CharField(max_length=64) 
    disassembled = models.CharField(max_length=64) # persian # moving the calendar from english to persian
    supplying_or_manufacturing = models.CharField(max_length=16)
    internal_or_external_outsourcing = models.CharField(max_length=64) 
    vendor = models.CharField(max_length=64) 
    joining = models.CharField(max_length=64) 
    manufacturing_process = models.CharField(max_length=256)
    raw_material_form = models.CharField(max_length=64) 
    function = models.CharField(max_length=64)
    qc_criteria = models.CharField(max_length=32)
    manufacturing_priority = models.CharField(max_length=64) 
    manufacturing_responsible_department = models.CharField(max_length=16) # relational to user groups
    designing_responsible_department = models.CharField(max_length=32)
    usage_on_other_engines = models.CharField(max_length=64)
    manufacturing_parts_category = models.CharField(max_length=64)
    scope_matrix_category = models.CharField(max_length=64)
    requires_manufacturing_or_supplying_for_reassembly = models.CharField(max_length=64) 
    system_D_requirements = models.TextField(max_length=1024)
    percurment_state = models.CharField(max_length=64) 
    details = models.CharField(max_length=16) 
    joint_type = models.CharField(max_length=32)
    discarded_during_disassembly = models.CharField(max_length=32) 
    expendables = models.BooleanField()
    discarded_or_unusable_according_to_docs = models.CharField(max_length=32) 
    destroyed_for_analysis = models.CharField(max_length=32) 
    rejected_by_qc_or_inspection = models.CharField(max_length=32)
    class_size_or_weight_as_required = models.CharField(max_length=32)
    EBOM = models.IntegerField()

    class Meta:
        permissions = list(zip(permission_codes, permission_names))

    # def __str__(self):
    #     return self.ID
    

class FieldPermission(models.Model):
    model = models.CharField(max_length=64, null=True, blank=True)
    instance_id = models.IntegerField(null=True, blank=True)
    FIELD_CHOISES = [
        ('all', 'all'),
        ('revision', 'revision'),
        ('ID', 'ID'),
        ('P_on_N_status_code', 'P_on_N_status_code'),
        ('fig_no', 'fig_no'),
        ('item_no', 'item_no'),
        ('module', 'module'),
        ('level', 'level'),
        ('code', 'code'),
        ('parent_code', 'parent_code'),
        ('part_number', 'part_number'),
        ('description', 'description'),
        ('comment', 'comment'),
        ('sap_name', 'sap_name'),
        ('unit_per_assy', 'unit_per_assy'),
        ('unit_per_end_item', 'unit_per_end_item'),
        ('corrected_units_per_end_item', 'corrected_units_per_end_item'),
        ('gg_qty', 'gg_qty'),
        ('srp', 'srp'),
        ('store_comment', 'store_comment'),
        ('assembly', 'assembly'),
        ('standard_part', 'standard_part'),
        ('material', 'material'),
        ('mfg_complexity_level', 'mfg_complexity_level'),
        ('disassembled', 'disassembled'),
        ('supplying_or_manufacturing', 'supplying_or_manufacturing'),
        ('internal_or_external_outsourcing', 'internal_or_external_outsourcing'),
        ('vendor', 'vendor'),
        ('joining', 'joining'),
        ('manufacturing_process', 'manufacturing_process'),
        ('raw_material_form', 'raw_material_form'),
        ('function', 'function'),
        ('qc_criteria', 'qc_criteria'),
        ('manufacturing_priority', 'manufacturing_priority'),
        ('manufacturing_responsible_department', 'manufacturing_responsible_department'),
        ('designing_responsible_department', 'designing_responsible_department'),
        ('usage_on_other_engines', 'usage_on_other_engines'),
        ('manufacturing_parts_category', 'manufacturing_parts_category'),
        ('scope_matrix_category', 'scope_matrix_category'),
        ('requires_manufacturing_or_supplying_for_reassembly', 'requires_manufacturing_or_supplying_for_reassembly'),
        ('system_D_requirements', 'system_D_requirements'),
        ('percurment_state', 'percurment_state'),
        ('details', 'details'),
        ('joint_type', 'joint_type'),
        ('discarded_during_disassembly', 'discarded_during_disassembly'),
        ('expendables', 'expendables'),
        ('discarded_or_unusable_according_to_docs', 'discarded_or_unusable_according_to_docs'),
        ('destroyed_for_analysis', 'destroyed_for_analysis'),
        ('rejected_by_qc_or_inspection', 'rejected_by_qc_or_inspection'),
        ('class_size_or_weight_as_required', 'class_size_or_weight_as_required'),
        ('EBOM', 'EBOM'),
    ]
    field = models.CharField(max_length=128, null=True, blank=True, choices=FIELD_CHOISES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    METHOD_CHOISES = [
        ('list', 'list'),
        ('create', 'create'),
        ('retrieve', 'retrieve'),
        ('retrieve_column', 'retrieve_column'),
        ('update', 'update'),
        ('update_column', 'update_column'),
        ('partial_update', 'partial_update'),
        ('destroy', 'destroy'),
    ]
    method = models.CharField(max_length=64, choices=METHOD_CHOISES)

    def __str__(self):
        if self.method in ['list', 'create']:
            return f'group: {self.group}, method: {self.method}'
        else:
            return f'group: {self.group}, method: {self.method}, model: {self.model}, field: {self.field}, instance_id: {self.instance_id}'
