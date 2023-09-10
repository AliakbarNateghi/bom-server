from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
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

    """
    <--->
    """

    # APPLICATION_TYPE_CHOISE = [
    #     ("contract", "contract"),
    #     ("purchase_report", "purchase_report"),
    # ]
    # APPLICATION_TYPE_CHOISE = [
    #     ("contract", "قرارداد"),
    #     ("contractor", "پیمانکار"),
    # ]
    APPLICATION_TYPE_CHOISE = [
        ("قرارداد", "قرارداد"),
        ("پیمانکار", "پیمانکار"),
    ]
    application_type = models.CharField(
        null=True, blank=True, choices=APPLICATION_TYPE_CHOISE, max_length=32
    )  # نوع درخواست
    """
    <--->
    """

    """
    <--->
    """
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
    # SUPPLY_STAGE_CHOISE = [
    #     (
    #         "find_contractors_and_qualifications",
    #         "یافتن پیمانكاران و تایید صلاحیت پیمانكار",
    #     ),
    #     ("request_for_inquiry/tender", "درخواست استعلام/مناقصه"),
    #     ("receive_price/payment_proposal", "دریافت پیشنهاد قیمت/پاكات"),
    #     (
    #         "receive_technical_approval_from_requesting_unit",
    #         "دریافت تایید فنی از واحد درخواست دهنده",
    #     ),
    #     (
    #         "transaction_commission_report/purchase_report",
    #         "تهیه گزارش كمیسیون معاملات/گزارش خرید",
    #     ),
    #     ("organization_of_trading_commission", "برگزاری كمیسیون معاملات"),
    #     ("approval_of_transactions_commission", "تایید كمیسیون معاملات"),
    #     ("order_notification", "ابلاغ سفارش"),
    #     ("preparation_of_draft_contract", "تهیه پیش نویس قرارداد"),
    #     (
    #         "approval_of_draft_contract_by_applicant",
    #         "تایید پیش نویس قرارداد توسط درخواست دهنده",
    #     ),
    #     ("signature_of_contractor", "امضای پیمانكار"),
    #     ("internal_signature", "امضای داخلی"),
    #     ("contract_notification", "ابلاغ قرارداد"),
    #     ("delivered", "تحویل گردید"),
    #     ("deleted", "حذف شد"),
    #     ("receive_guarantees", "دریافت تضامین"),
    #     ("reference_to_finance", "ارجاع به مالی"),
    # ]
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
    """
    <--->
    """

    """
    <--->
    """
    # MATERIAL_SUPPLIER_CHOISE = [
    #     ("contractor", "contractor"),
    #     ("employer", "employer"),
    # ]
    # MATERIAL_SUPPLIER_CHOISE = [
    #     ("contractor", "پیمانکار"),
    #     ("employer", "کارفرما"),
    # ]
    MATERIAL_SUPPLIER_CHOISE = [
        ("پیمانکار", "پیمانکار"),
        ("کارفرما", "کارفرما"),
    ]
    material_supplier = models.CharField(
        null=True, blank=True, choices=MATERIAL_SUPPLIER_CHOISE, max_length=32
    )
    """
    <--->
    """

    pr = models.BigIntegerField(null=True, blank=True)
    po = models.IntegerField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True, max_length=512)

    """
    <--->
    """
    # REQUEST_TYPE_CHOISE = [
    #     ("raw_material", "ماده اولیه"),
    #     ("semi_finished", "ماده نیمه آماده"),
    #     ("component_supply", "تامین قطعه"),
    #     ("manufacturing", "ساخت"),
    #     ("tools_and_machinery", "ابزار و ماشین آلات"),
    #     ("service", "خدمت"),
    # ]
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
    """
    <--->
    """

    """
    <--->
    """
    # customer_management = models.ForeignKey(
    #     Department,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name="customer_management",
    # )
    # CUSTOMER_MANAGEMENT_CHOISE = [
    #     ("fan_and_compressor", "فن و کمپرسور"),
    #     ("lateral", "جانبی"),
    #     ("turbine", "توربین"),
    #     ("minor_part", "ماینور پارت"),
    #     ("combustion_chamber", "محفظه احتراق"),
    #     ("engine_structure_design", "طراحی سازه موتور"),
    #     ("standard_and_quality", "استاندارد و كیفیت"),
    # ]
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
    """
    <--->
    """

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

    """
    <--->
    """
    # CURRENCY_CHOISE = [
    #     ("rial", "ریال"),
    #     ("euro", "یورو"),
    #     ("dollar", "دلار"),
    #     ("yuan", "یوان"),
    #     ("dirham", "درهم"),
    # ]
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
    """
    <--->
    """

    """
    <--->
    """
    # expert = models.ForeignKey(BomUser, null=True, blank=True, on_delete=models.CASCADE)
    # EXPERT_CHOISE = [
    #     ("ghaniabadi", "غنی آبادی"),
    #     ("mohammadzadeh", "محمد زاده"),
    #     ("roshandel", "روشن دل"),
    # ]
    EXPERT_CHOISE = [
        ("غنی آبادی", "غنی آبادی"),
        ("محمد زاده", "محمد زاده"),
        ("روشن دل", "روشن دل"),
    ]
    expert = models.CharField(
        null=True, blank=True, max_length=64, choices=EXPERT_CHOISE
    )
    """
    <--->
    """

    prepayment_percentage = models.IntegerField(
        validators=PERCENTAGE_VALIDATOR, null=True, blank=True
    )
    currency_type = models.CharField(null=True, blank=True, max_length=64)
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

    """
    <--->
    """
    # FINANCIAL_SITUATION_CHOISE = [
    #     ("receiving_guarantees", "دریافت تضامین"),
    #     ("prepayment_request", "درخواست پیش پرداخت"),
    #     ("determining_the_type_of_currency", "تعیین نوع ارز"),
    #     ("agreement_with_the_supplier", "توافق با تامین كننده"),
    #     ("receiving_currency_documents", "دریافت مستندات ارزی"),
    #     ("currency_request_from_mapna_international", "درخواست ارز از مپنا بین الملل"),
    #     ("sending_documents_to_mapna_international", "ارسال مدارك به مپنا بین الملل"),
    #     ("tracking_currency_request", "پیگیری درخواست ارز"),
    #     ("paid", "پرداخت شده"),
    # ]
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
    """
    <--->
    """

    # prepayment_request_date = JalaliDateField()
    prepayment_request_date = models.CharField(null=True, blank=True, max_length=10)

    prepayment_amount = models.BigIntegerField(null=True, blank=True)

    # prepayment_date = JalaliDateField()
    prepayment_date = models.CharField(null=True, blank=True, max_length=10)


class ProvideFieldPermission(models.Model):
    instance_id = models.IntegerField(null=True, blank=True)
    # FIELD_CHOISES = [
    #     ("نوع درخواست (گزارش خرید/قرارداد)", "نوع درخواست (گزارش خرید/قرارداد)"),
    #     ("مرحله تامین", "مرحله تامین"),
    #     ("تامین كننده متریال", "تامین كننده متریال"),
    #     ("شماره PR", "شماره PR"),
    #     ("شماره PO", "شماره PO"),
    #     ("موضوع", "موضوع"),
    #     ("جنس درخواست", "جنس درخواست"),
    #     ("مدیریت سفارش دهنده", "مدیریت سفارش دهنده"),
    #     ("شماره قرارداد", "شماره قرارداد"),
    #     ("تامین كننده", "تامین كننده"),
    #     ("مبلغ", "مبلغ"),
    #     ("مبلغ تعدیل", "مبلغ تعدیل"),
    #     (" جمع مبلغ ", " جمع مبلغ "),
    #     ("نوع ارز", "نوع ارز"),
    #     ("كارشناس مسئول", "كارشناس مسئول"),
    #     ("درصد پیش‌پرداخت", "درصد پیش‌پرداخت"),
    #     ("مبلغ پیش‌پرداخت طبق قرارداد", "مبلغ پیش‌پرداخت طبق قرارداد"),
    #     ("پیش پرداخت توسط توگا", "پیش پرداخت توسط توگا"),
    #     ("پیش پرداخت توسط موتور هوایی", "پیش پرداخت توسط موتور هوایی"),
    #     (" جمع پیش پرداخت ها- ریالی ", " جمع پیش پرداخت ها- ریالی "),
    #     (" چك تضمین پیش پرداخت ", " چك تضمین پیش پرداخت "),
    #     (" ضمانتنامه پیش پرداخت ", " ضمانتنامه پیش پرداخت "),
    #     (" ضمانت نامه سند رهنی ", " ضمانت نامه سند رهنی "),
    #     (" جمع ضمانت نامه های پیش پرداخت ", " جمع ضمانت نامه های پیش پرداخت "),
    #     ("وضعیت در معاونت مالی", "وضعیت در معاونت مالی"),
    #     ("تاریخ درخواست پیش پرداخت", "تاریخ درخواست پیش پرداخت"),
    #     ("مبلغ پیش پرداخت", "مبلغ پیش پرداخت"),
    #     ("نوع ارز", "نوع ارز"),
    #     ("تاریخ پرداخت پیش پرداخت", "تاریخ پرداخت پیش پرداخت"),
    # ]
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
