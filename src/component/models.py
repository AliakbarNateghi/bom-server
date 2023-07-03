from django.db import models

from ..core.models import BomBaseModel


class BomComponent(BomBaseModel):
    revision = models.IntegerField()
    ID = models.IntegerField()
    P_on_N_status_code = models.IntegerField()
    fig_no = models.CharField(max_length=16)
    item_no = models.IntegerField()
    module = models.CharField(max_length=16)
    level = models.IntegerField()
    part_number = models.CharField(max_length=128)
    description = models.CharField(max_length=16)
    unit_per_assy = models.IntegerField()
    unit_per_end_item = models.IntegerField()
    corrected_units_per_end_item = models.IntegerField()
    gg_qty = models.IntegerField() # check
    store_comment = models.TextField(max_length=1024)
    assembly = models.BooleanField(default=False)
    standard_part = models.BooleanField(default=False)
    material = models.CharField(max_length=64)
    mfg_complexity_level = models.CharField(max_length=64) # check
    disassembled = models.DateTimeField() # persian
    supplying_and_manufacturing = models.CharField(max_length=16)
    manufacturing_priority = models.CharField(max_length=64) # check
    manufacturing_responsible_department = models.CharField(max_length=16) # Should be choise or a relational to user groups
    designing_responsible_department = models.CharField(max_length=32)
    usage_on_other_engines = models.CharField(max_length=64)
    manufacturing_parts_category = models.CharField(max_length=64)
    scope_matrix_category = models.CharField(max_length=64)
    requires_manufacturing_or_supplying_for_reassembly = models.CharField(max_length=64) # check
    system_D_requirements = models.TextField(max_length=1024)
    percurment_state = models.CharField(max_length=64) # check
    details = models.CharField(max_length=16) # check
    joint_type = models.CharField(max_length=32)
    discarded_during_disassembly = models.CharField(max_length=32) # check
    expendables = models.BooleanField()
    discarded_or_unusable_according_to_docs = models.CharField(max_length=32) # check
    destroyed_for_analysis = models.CharField(max_length=32) # check
    rejected_by_qc_or_inspection = models.CharField(max_length=32) # check
    class_size_or_weight_as_required = models.CharField(max_length=32) # check
    EBOM = models.IntegerField()

