from django.contrib.auth.models import Group
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from jalali_date.fields import JalaliDateField

from ..core.models import BomBaseModel
from ..user.models import Department, BomUser

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

# RUD = [
#     "R_",
#     "U_",
#     "D_",
# ]  # CRUD without C

# retrieve_update_delete = [
#     "retrieve ",
#     "update ",
#     "delete ",
# ]

# permission_codes = []
# for method in RUD:
#     for field in fields:
#         permission_codes.append(method + field)
# permission_codes.append("C")  # permission of creating a new component !!!

# permission_names = []
# for method in retrieve_update_delete:
#     for field in fields:
#         permission_names.append(method + field)
# permission_names.append("create")


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
    # manufacturing_responsible_department = models.CharField(
    #     max_length=16, null=True, blank=True
    # )  # relational to user groups
    # designing_responsible_department = models.CharField(
    #     max_length=32, null=True, blank=True
    # )
    manufacturing_responsible_department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="manufacturing_responsible_department",
    )
    designing_responsible_department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="designing_responsible_department",
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

    # class Meta:
    #     permissions = list(zip(permission_codes, permission_names))


class BomFieldPermission(models.Model):
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
        return f"{self.group} {self.instance_id} {self.field}"


class ProvideComponent(BomBaseModel):
    # APPLICATION_TYPE_CHOISE = [
    #     ("contract", "contract"),
    #     ("purchase_report", "purchase_report"),
    # ]
    APPLICATION_TYPE_CHOISE = [
        ("قرارداد", "قرارداد"),
        ("پیمانکار", "پیمانکار"),
    ]
    application_type = models.CharField(
        null=True, blank=True, choices=APPLICATION_TYPE_CHOISE, max_length=32
    ) # نوع درخواست

    # SUPPLY_STAGE_CHOISE = [
    #     ("find_contractors_and_qualifications", "find_contractors_and_qualifications"),
    #     ("request_for_inquiry/tender", "request_for_inquiry/tender"),
    #     ("receive_price/payment_proposal", "receive_price/payment_proposal"),
    #     ("receive_technical_approval_from_requesting_unit", "receive_technical_approval_from_requesting_unit"),
    #     ("transaction_commission_report/purchase_report", "transaction_commission_report/purchase_report"),
    #     ("organization_of_trading_commission", "organization_of_trading_commission"),
    #     ("approval_of_transactions_commission", "approval_of_transactions_commission"),
    #     ("order_notification", "order_notification"),
    #     ("preparation_of_draft_contract", "preparation_of_draft_contract"),
    #     ("approval_of_draft_contract_by_applicant", "approval_of_draft_contract_by_applicant"),
    #     ("signature_of_contractor", "signature_of_contractor"),
    #     ("internal_signature", "internal_signature"),
    #     ("contract_notification", "contract_notification"),
    #     ("delivered", "delivered"),
    #     ("deleted", "deleted"),
    #     ("receive_guarantees", "receive_guarantees"),
    #     ("reference_to_finance", "reference_to_finance"),
    # ]
    SUPPLY_STAGE_CHOISE = [
        (
            "يافتن پيمانكاران و تاييد صلاحيت پيمانكار",
            "يافتن پيمانكاران و تاييد صلاحيت پيمانكار",
        ),
        ("درخواست استعلام/مناقصه", "درخواست استعلام/مناقصه"),
        ("دريافت پيشنهاد قيمت/پاكات", "دريافت پيشنهاد قيمت/پاكات"),
        (
            "دريافت تاييد فني از واحد درخواست دهنده",
            "دريافت تاييد فني از واحد درخواست دهنده",
        ),
        (
            "تهيه گزارش كميسيون معاملات/گزارش خريد",
            "تهيه گزارش كميسيون معاملات/گزارش خريد",
        ),
        ("برگزاري كميسيون معاملات", "برگزاري كميسيون معاملات"),
        ("تاييد كميسيون معاملات", "تاييد كميسيون معاملات"),
        ("ابلاغ سفارش", "ابلاغ سفارش"),
        ("تهيه پيش نويس قرارداد", "تهيه پيش نويس قرارداد"),
        (
            "تاييد پيش نويس قرارداد توسط درخواست دهنده",
            "تاييد پيش نويس قرارداد توسط درخواست دهنده",
        ),
        ("امضاي پيمانكار", "امضاي پيمانكار"),
        ("امضاي داخلي", "امضاي داخلي"),
        ("ابلاغ قرارداد", "ابلاغ قرارداد"),
        ("تحويل گرديد", "تحويل گرديد"),
        ("حذف شد", "حذف شد"),
        ("دريافت تضامين", "دريافت تضامين"),
        (" ارجاع به مالي", " ارجاع به مالي"),
    ]
    supply_stage = models.TextField(
        null=True, blank=True, max_length=512, choices=SUPPLY_STAGE_CHOISE
    )
    # MATERIAL_SUPPLIER_CHOISE = [
    #     ("contracter", "contracter"),
    #     ("employer", "employer"),
    # ]
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
        ("ماده اوليه", "ماده اوليه"),
        ("ماده نيمه آماده", "ماده نيمه آماده"),
        ("تامين قطعه", "تامين قطعه"),
        ("ساخت", "ساخت"),
        ("ابزار و ماشين آلات", "ابزار و ماشين آلات"),
        ("خدمت", "خدمت"),
    ]
    request_type = models.CharField(
        null=True, blank=True, max_length=128, choices=REQUEST_TYPE_CHOISE
    ) # جنس درخواست
    customer_management = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="customer_management",
    )
    contract_number = models.BigIntegerField(null=True, blank=True)
    supplier = models.CharField(null=True, blank=True, max_length=64)

    """
    <--- SUM --->
    """
    amount = models.BigIntegerField(null=True, blank=True)
    adjustment_amount = models.BigIntegerField(null=True, blank=True)
    """
    <--- SUM --->
    """

    CURRENCY_CHOISE = [
        ("ریال", "ریال"),
        ("يورو", "يورو"),
        ("دلار", "دلار"),
        ("يوان", "يوان"),
        ("درهم", "درهم"),
    ]
    currency = models.CharField(null=True, blank=True, max_length=16, choices=CURRENCY_CHOISE)
    expert = models.ForeignKey(BomUser, null=True, blank=True, on_delete=models.CASCADE)
    prepayment_percentage = models.IntegerField(validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    prepayment_according_to_contract = models.BigIntegerField(null=True, blank=True)

    """
    <--- SUM --->
    """
    prepaid_by_toga = models.BigIntegerField(null=True, blank=True)
    prepaid_by_air_engine = models.BigIntegerField(null=True, blank=True)
    """
    <--- SUM --->
    """

    prepayment_guarantee_check = models.CharField(null=True, blank=True, max_length=64)
    prepayment_guarantee = models.BigIntegerField(null=True, blank=True)
    mortgage_document_guarantee = models.BigIntegerField(null=True, blank=True)
    # sum_of_prepayment_guarantees = models.BigIntegerField(null=True, blank=True)
    FINANCIAL_SITUATION_CHOISE = [
        ("دريافت تضامين", "دريافت تضامين"),
        ("درخواست پيش پرداخت", "درخواست پيش پرداخت"),
        ("تعيين نوع ارز", "تعيين نوع ارز"),
        ("توافق با تامين كننده", "توافق با تامين كننده"),
        ("دريافت مستندات ارزي", "دريافت مستندات ارزي"),
        ("درخواست ارز از مپنا بين الملل", "درخواست ارز از مپنا بين الملل"),
        ("ارسال مدارك به مپنا بين الملل", "ارسال مدارك به مپنا بين الملل"),
        ("پيگيري درخواست ارز", "پيگيري درخواست ارز"),
        ("پرداخت شده", "پرداخت شده"),
    ]
    financial_situation = models.CharField(
        null=True, blank=True, max_length=64, choices=FINANCIAL_SITUATION_CHOISE
    )
    prepayment_request_date = JalaliDateField()
    prepayment_amount = models.BigIntegerField(null=True, blank=True)
    prepayment_date = JalaliDateField()


class ProvideFieldPermission(models.Model):
    instance_id = models.IntegerField(null=True, blank=True)
    FIELD_CHOISES = [
        ("نوع درخواست (گزارش خريد/قرارداد)", "نوع درخواست (گزارش خريد/قرارداد)"),
        ("مرحله تامين", "مرحله تامين"),
        ("تامين كننده متريال", "تامين كننده متريال"),
        ("شماره PR", "شماره PR"),
        ("شماره PO", "شماره PO"),
        ("موضوع", "موضوع"),
        ("جنس درخواست", "جنس درخواست"),
        ("مديريت سفارش دهنده", "مديريت سفارش دهنده"),
        ("شماره قرارداد", "شماره قرارداد"),
        ("تامين كننده", "تامين كننده"),
        ("مبلغ", "مبلغ"),
        ("مبلغ تعديل", "مبلغ تعديل"),
        (" جمع مبلغ ", " جمع مبلغ "),
        ("نوع ارز", "نوع ارز"),
        ("كارشناس مسئول", "كارشناس مسئول"),
        ("درصد پيش‌پرداخت", "درصد پيش‌پرداخت"),
        ("مبلغ پيش‌پرداخت طبق قرارداد", "مبلغ پيش‌پرداخت طبق قرارداد"),
        ("پيش پرداخت توسط توگا", "پيش پرداخت توسط توگا"),
        ("پيش پرداخت توسط موتور هوايي", "پيش پرداخت توسط موتور هوايي"),
        (" جمع پيش پرداخت ها- ريالي ", " جمع پيش پرداخت ها- ريالي "),
        (" چك تضمين پيش پرداخت ", " چك تضمين پيش پرداخت "),
        (" ضمانتنامه پيش پرداخت ", " ضمانتنامه پيش پرداخت "),
        (" ضمانت نامه سند رهني ", " ضمانت نامه سند رهني "),
        (" جمع ضمانت نامه هاي پيش پرداخت ", " جمع ضمانت نامه هاي پيش پرداخت "),
        ("وضعيت در معاونت مالي", "وضعيت در معاونت مالي"),
        ("تاريخ درخواست پيش پرداخت", "تاريخ درخواست پيش پرداخت"),
        ("مبلغ پيش پرداخت", "مبلغ پيش پرداخت"),
        ("نوع ارز", "نوع ارز"),
        ("تاريخ پرداخت پيش پرداخت", "تاريخ پرداخت پيش پرداخت"),
    ]
    field = models.CharField(
        max_length=128, null=True, blank=True, choices=FIELD_CHOISES
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    editable = models.BooleanField()

    def __str__(self):
        return f"{self.group} {self.instance_id} {self.field}"
