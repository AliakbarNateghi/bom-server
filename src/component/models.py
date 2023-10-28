from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from jalali_date.fields import JalaliDateField

from ..core.models import BomBaseModel
from ..user.models import BomUser, Department

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

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
    )  # relational to user departments
    designing_responsible_department = models.CharField(
        max_length=32, null=True, blank=True
    )  # relational to user departments

    # manufacturing_responsible_department = models.ForeignKey(
    #     Department,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name="manufacturing_responsible_department",
    # )
    # designing_responsible_department = models.ForeignKey(
    #     Department,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name="designing_responsible_department",
    # )
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

    # class Meta:
    #     permissions = list(zip(permission_codes, permission_names))


class BomFieldPermission(models.Model):
    instance_id = models.IntegerField(null=True, blank=True)
    FIELD_CHOISES = [
        ("revision", "revision"),
        ("ID", "ID"),
        ("P_on_N_status_code", "P/N Status Code"),
        ("fig_no", "Fig. No."),
        ("item_no", "Item No."),
        ("module", "Module"),
        ("level", "Level"),
        ("code", "Code"),
        ("parent_code", "Parent Code"),
        ("part_number", "Part Number"),
        ("description", "Description"),
        ("comment", "Comment"),
        ("sap_name", "SAP NAME"),
        ("unit_per_assy", "Units Per Assy"),
        ("unit_per_end_item", "Units Per End Item"),
        ("corrected_units_per_end_item", "Corrected Units Per End Item"),
        ("gg_qty", "GG QTY"),
        ("srp", "SRP"),
        ("store_comment", "Store Comment"),
        ("assembly", "Assembly"),
        ("standard_part", "Standard Part"),
        ("material", "Material"),
        ("mfg_complexity_level", "Mfg. Complexity Level"),
        ("disassembled", "Disassembled"),
        ("supplying_or_manufacturing", "Supplying / Manufacturing "),
        ("internal_or_external_outsourcing", "Internal / External outsourcing"),
        ("vendor", "Vendor"),
        ("joining", "Joining"),
        ("manufacturing_process", "Manufacturing Process"),
        ("raw_material_form", "Raw Material Form"),
        ("function", "Function"),
        ("qc_criteria", "QC Criteria"),
        ("manufacturing_priority", "Manufacturing Priority "),
        (
            "manufacturing_responsible_department",
            "Manufacturing Responsible Department",
        ),
        ("designing_responsible_department", "Designing Responsible Department"),
        ("usage_on_other_engines", "USAGE ON OTHER ENGINES"),
        ("manufacturing_parts_category", "MANUFACTURING PARTS Category"),
        ("scope_matrix_category", "Scope Matrix Category"),
        (
            "requires_manufacturing_or_supplying_for_reassembly",
            "Requires Manufacturing/Supplying For Re-Assembly",
        ),
        ("system_D_requirements", "System D. Requirement"),
        ("percurment_state", "PERCURMENT STATE"),
        ("details", "DETAILS"),
        ("joint_type", "Joint Type"),
        ("discarded_during_disassembly", "DISCARDED DURING DISSASSEMBLY"),
        ("expendables", "Expendables"),
        (
            "discarded_or_unusable_according_to_docs",
            "Discarded/Unusable According To Docs",
        ),
        ("destroyed_for_analysis", "Destroyed For Analysis"),
        ("rejected_by_qc_or_inspection", "Rejected by QC/Inspection"),
        ("class_size_or_weight_as_required", "Class Size/Weight As Required"),
        ("EBOM", "EBOM"),
    ]
    field = models.CharField(
        max_length=128, null=True, blank=True, choices=FIELD_CHOISES
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    editable = models.BooleanField()

    def __str__(self):
        return f"{self.group} {self.instance_id} {self.field}"


class ProvideComponent(BomBaseModel):
    APPLICATION_TYPE_CHOISE = [
        ("قرارداد", "قرارداد"),
        ("پیمانکار", "پیمانکار"),
    ]
    application_type = models.CharField(
        null=True, blank=True, choices=APPLICATION_TYPE_CHOISE, max_length=32
    )  # نوع درخواست

    SUPPLY_STAGE_CHOISE = [
        (
            "یافتن پیمانكاران و تایید صلاحیت پیمانكار",
            "یافتن پیمانكاران و تایید صلاحیت پیمانكار",
        ),
        ("درخواست استعلام/مناقصه", "درخواست استعلام/مناقصه"),
        ("دریافت پیشنهاد قیمت/پاكات", "دریافت پیشنهاد قیمت/پاكات"),
        (
            "دریافت تایید فنی از واحد درخواست دهنده",
            "دریافت تایید فنی از واحد درخواست دهنده",
        ),
        (
            "تهیه گزارش كمیسیون معاملات/گزارش خرید",
            "تهیه گزارش كمیسیون معاملات/گزارش خرید",
        ),
        ("برگزاری كمیسیون معاملات", "برگزاری كمیسیون معاملات"),
        ("تایید كمیسیون معاملات", "تایید كمیسیون معاملات"),
        ("ابلاغ سفارش", "ابلاغ سفارش"),
        ("تهیه پیش نویس قرارداد", "تهیه پیش نویس قرارداد"),
        (
            "تایید پیش نویس قرارداد توسط درخواست دهنده",
            "تایید پیش نویس قرارداد توسط درخواست دهنده",
        ),
        ("امضای پیمانكار", "امضای پیمانكار"),
        ("امضای داخلی", "امضای داخلی"),
        ("ابلاغ قرارداد", "ابلاغ قرارداد"),
        ("تحویل گردید", "تحویل گردید"),
        ("حذف شد", "حذف شد"),
        ("دریافت تضامین", "دریافت تضامین"),
        ("ارجاع به مالی", "ارجاع به مالی"),
    ]
    supply_stage = models.TextField(
        null=True, blank=True, max_length=512, choices=SUPPLY_STAGE_CHOISE
    )
    MATERIAL_SUPPLIER_CHOISE = [
        ("پیمانکار", "پیمانکار"),
        ("کارفرما", "کارفرما"),
    ]
    material_supplier = models.CharField(
        null=True, blank=True, choices=MATERIAL_SUPPLIER_CHOISE, max_length=32
    )
    pr = models.BigIntegerField(null=True, blank=True)
    po = models.IntegerField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True, max_length=512)
    REQUEST_TYPE_CHOISE = [
        ("ماده اولیه", "ماده اولیه"),
        ("ماده نیمه آماده", "ماده نیمه آماده"),
        ("تامین قطعه", "تامین قطعه"),
        ("ساخت", "ساخت"),
        ("ابزار و ماشین آلات", "ابزار و ماشین آلات"),
        ("خدمت", "خدمت"),
    ]
    request_type = models.CharField(
        null=True, blank=True, max_length=128, choices=REQUEST_TYPE_CHOISE
    )  # جنس درخواست

    # customer_management = models.ForeignKey(
    #     Department,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name="customer_management",
    # )

    CUSTOMER_MANAGEMENT_CHOISE = [
        ("فن و کمپرسور", "فن و کمپرسور"),
        ("جانبی", "جانبی"),
        ("توربین", "توربین"),
        ("ماینور پارت", "ماینور پارت"),
        ("محفظه احتراق", "محفظه احتراق"),
        ("طراحی سازه موتور", "طراحی سازه موتور"),
        ("استاندارد و كیفیت", "استاندارد و كیفیت"),
    ]
    customer_management = models.CharField(
        null=True, blank=True, max_length=128, choices=CUSTOMER_MANAGEMENT_CHOISE
    )
    contract_number = models.BigIntegerField(null=True, blank=True)
    supplier = models.CharField(null=True, blank=True, max_length=64)
    amount = models.BigIntegerField(null=True, blank=True)
    adjustment_amount = models.BigIntegerField(null=True, blank=True)
    CURRENCY_CHOISE = [
        ("ریال", "ریال"),
        ("یورو", "یورو"),
        ("دلار", "دلار"),
        ("یوان", "یوان"),
        ("درهم", "درهم"),
    ]
    currency = models.CharField(
        null=True, blank=True, max_length=16, choices=CURRENCY_CHOISE
    )
    EXPERT_CHOISE = [
        ("غنی آبادی", "غنی آبادی"),
        ("محمد زاده", "محمد زاده"),
        ("روشن دل", "روشن دل"),
    ]
    expert = models.CharField(
        null=True, blank=True, max_length=64, choices=EXPERT_CHOISE
    )
    prepayment_percentage = models.IntegerField(
        validators=PERCENTAGE_VALIDATOR, null=True, blank=True
    )
    currency_type = models.CharField(null=True, blank=True, max_length=64)
    prepayment_according_to_contract = models.BigIntegerField(null=True, blank=True)
    prepaid_by_toga = models.BigIntegerField(null=True, blank=True)
    prepaid_by_air_engine = models.BigIntegerField(null=True, blank=True)
    prepayment_guarantee_check = models.CharField(null=True, blank=True, max_length=64)
    prepayment_guarantee = models.BigIntegerField(null=True, blank=True)
    mortgage_document_guarantee = models.BigIntegerField(null=True, blank=True)
    # sum_of_prepayment_guarantees = models.BigIntegerField(null=True, blank=True)

    FINANCIAL_SITUATION_CHOISE = [
        ("دریافت تضامین", "دریافت تضامین"),
        ("درخواست پیش پرداخت", "درخواست پیش پرداخت"),
        ("تعیین نوع ارز", "تعیین نوع ارز"),
        ("توافق با تامین كننده", "توافق با تامین كننده"),
        ("دریافت مستندات ارزی", "دریافت مستندات ارزی"),
        ("درخواست ارز از مپنا بین الملل", "درخواست ارز از مپنا بین الملل"),
        ("ارسال مدارك به مپنا بین الملل", "ارسال مدارك به مپنا بین الملل"),
        ("پیگیری درخواست ارز", "پیگیری درخواست ارز"),
        ("پرداخت شده", "پرداخت شده"),
    ]
    financial_situation = models.CharField(
        null=True, blank=True, max_length=64, choices=FINANCIAL_SITUATION_CHOISE
    )

    # prepayment_request_date = JalaliDateField()
    prepayment_request_date = models.CharField(null=True, blank=True, max_length=10)
    prepayment_amount = models.BigIntegerField(null=True, blank=True)

    # prepayment_date = JalaliDateField()
    prepayment_date = models.CharField(null=True, blank=True, max_length=10)

    
class ProvideFieldPermission(models.Model):
    instance_id = models.IntegerField(null=True, blank=True)
    FIELD_CHOISES = [
        ("application_type", "application_type"),
        ("supply_stage", "supply_stage"),
        ("material_supplier", "material_supplier"),
        ("pr", "pr"),
        ("po", "po"),
        ("subject", "subject"),
        ("request_type", "request_type"),
        ("customer_management", "customer_management"),
        ("contract_number", "contract_number"),
        ("supplier", "supplier"),
        ("amount", "amount"),
        ("adjustment_amount", "adjustment_amount"),
        ("currency", "currency"),
        ("expert", "expert"),
        ("prepayment_percentage", "prepayment_percentage"),
        ("currency_type", "currency_type"),
        ("prepayment_according_to_contract", "prepayment_according_to_contract"),
        ("prepaid_by_toga", "prepaid_by_toga"),
        ("prepaid_by_air_engine", "prepaid_by_air_engine"),
        ("prepayment_guarantee_check", "prepayment_guarantee_check"),
        ("prepayment_guarantee", "prepayment_guarantee"),
        ("mortgage_document_guarantee", "mortgage_document_guarantee"),
        ("financial_situation", "financial_situation"),
        ("prepayment_request_date", "prepayment_request_date"),
        ("prepayment_amount", "prepayment_amount"),
        ("prepayment_date", "prepayment_date"),
    ]
    field = models.CharField(
        max_length=128, null=True, blank=True, choices=FIELD_CHOISES
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    editable = models.BooleanField()

    def __str__(self):
        return f"{self.group} {self.instance_id} {self.field}"
    

class OriginalReportCore(BomBaseModel):
    original_report_id = models.IntegerField(null=True, blank=True)
    fig_no = models.CharField(max_length=16, null=True, blank=True)
    item_no = models.IntegerField(null=True, blank=True)
    module = models.CharField(max_length=16, null=True, blank=True)
    TUGA_subtitute_part_number = models.CharField(max_length=64, null=True, blank=True)
    old_system_part_no = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    unit_per_end_item = models.IntegerField(null=True, blank=True)
    assembly = models.BooleanField(default=False, null=True, blank=True)
    standard_part = models.BooleanField(default=False, null=True, blank=True)
    new_manufacturing_responsible_department = models.CharField(
        max_length=16, null=True, blank=True
    )
    level = models.CharField(max_length=32, null=True, blank=True)


class Design(BomBaseModel):
    disassembled = models.CharField(max_length=32, null=True, blank=True)
    progress_certificate = models.CharField(max_length=32, null=True, blank=True)
    ThreeD_scan_progress = models.CharField(max_length=32, null=True, blank=True)
    ThreeD_scan_certificate = models.CharField(max_length=32, null=True, blank=True)
    Fi_100_percent_l_modelling = models.CharField(max_length=32, null=True, blank=True)
    Fi_100_percent_l_modelling_certificate = models.CharField(max_length=32, null=True, blank=True)
    level_2_drawing = models.CharField(max_length=32, null=True, blank=True)
    level_2_drawing_certificate = models.CharField(max_length=32, null=True, blank=True)
    level_3_drawing = models.CharField(max_length=32, null=True, blank=True)
    level_3_drawing_certificate = models.CharField(max_length=32, null=True, blank=True)
    assembly_drawing = models.CharField(max_length=32, null=True, blank=True)
    construction_plan_with_assembly_view = models.CharField(max_length=32, null=True, blank=True)
    certificate_code = models.CharField(max_length=32, null=True, blank=True)

