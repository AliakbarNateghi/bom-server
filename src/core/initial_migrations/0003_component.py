import os
import random

import numpy as np
import pandas as pd
from django.db import migrations

script_dir = os.path.dirname(os.path.abspath(__file__))


def check_NaN(var):
    return None if pd.isna(var) else var


def create_default_group(apps, schema_editor):
    BomComponent = apps.get_model("component", "BomComponent")
    # Department = apps.get_model("user", "Department")
    ProvideComponent = apps.get_model("component", "ProvideComponent")
    PROVIDEdf = pd.read_excel(os.path.join(script_dir, "..", "data", "provide.xlsx"))
    # PROVIDEdf = PROVIDEdf.fillna(value=0)
    BOMdf = pd.read_excel(os.path.join(script_dir, "..", "data", "EBOM.xlsx"))
    # BOMdf = BOMdf.fillna(value=0)
    ScopeComponent = apps.get_model("component", "ScopeMatrix")
    # core_df = pd.read_excel(os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")), sheet_name="گزارش اصلي")
    design_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="طراحي",
    )
    # lateral_df = pd.read_excel(os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")), sheet_name="جانبي")
    manufacturing_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="ساخت",
    )
    _2_devices_side_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="جانبي دو دستگاه",
    )
    _28_devices_side_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="جانبي 28 دستگاه",
    )
    _2_devices_manufacturing_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="ساخت دو دستگاه",
    )
    _28_devices_manufacturing_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="ساخت 28 دستگاه",
    )
    _2_devices_quality_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="كيفيت دو دستگاه",
    )
    _28_devices_quality_df = pd.read_excel(
        os.path.join(os.path.join(script_dir, "..", "data", "scope.xlsx")),
        sheet_name="كيفيت 28 دستگاه",
    )

    # .iloc[1:]
    # designing_responsible_department = Department.objects.get(name__icontains=row["Designing Responsible Department"].replace(" ", ""))
    # manufacturing_responsible_department = Department.objects.get(name__icontains=row[
    #         "Manufacturing Responsible Department"
    #     ].replace(" ", ""))

    for index, row in design_df.iterrows():
        ScopeComponent.objects.create(
            original_report_id=check_NaN(row["ID"]),
            fig_no=check_NaN(row["Fig. No."]),
            item_no=check_NaN(row["Item No."]),
            module=check_NaN(row["Module"]),
            TUGA_subtitute_part_number=check_NaN(row["TUGA Substitute Part Number"]),
            old_system_part_no=check_NaN(row["Old System Part No."]),
            description=check_NaN(row["Description"]),
            unit_per_end_item=check_NaN(row["Units Per End Item"]),
            assembly=True if check_NaN(row["Assembly"]) in ["yes", "YES"] else False,
            standard_part=True if check_NaN(row["Standard Part"]) else False,
            new_manufacturing_responsible_department=check_NaN(
                row["New Manufacturing Responsible Department"]
            ),
            level=check_NaN(row["Level"]),
            disassembled=check_NaN(row["Disassembled"]),
            progress_certificate=check_NaN(row[" شناسنامه پیشرفت"]),
            ThreeD_scan_progress=check_NaN(row["3D Scan پیشرفت "]),
            ThreeD_scan_certificate=check_NaN(row["3D Scan مدرك "]),
            Fi_100_percent_l_modelling=check_NaN(row["Fi100%l Modelling"]),
            Fi_100_percent_l_modelling_certificate=check_NaN(
                row["Fi100%l Modelling مدرك"]
            ),
            level_2_drawing=check_NaN(row["Level 2 Drawing"]),
            level_2_drawing_certificate=check_NaN(row["Level 2 Drawing مدرك"]),
            level_3_drawing=check_NaN(row["Level 3 Drawing"]),
            level_3_drawing_certificate=check_NaN(row["Level 3 Drawing مدرك"]),
            assembly_drawing=check_NaN(row["Assembly Drawing"]),
            construction_plan_with_assembly_view=check_NaN(
                row["نقشه ساخت با نگرش مونتاژی"]
            ),
            certificate_code=check_NaN(row["كد مدرك شناسنامه"]),
        )

    cols = manufacturing_df.columns
    rating_col = cols[cols.str.contains("OPC", na=False)].item()
    for index, value in manufacturing_df[rating_col].items():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.OPC_or_MPP_rating = value
        scope_component.save()

    for index, row in manufacturing_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.identification_report_metallurgical_notebook_of_the_piece = (
            check_NaN(row["گزارش شناسايي (دفترچه متالوژيكي قطعه)"])
        )
        scope_component.identification_report_metallurgical_notebook_of_the_piece_certi = check_NaN(
            row["گزارش شناسايي (دفترچه متالوژيكي قطعه) مدرك"]
        )
        scope_component.raw_material_spec = check_NaN(row["اسپك ماده خام"])
        scope_component.raw_material_spec_certificate = check_NaN(
            row["اسپك ماده خام مدرك"]
        )
        scope_component.part_spec = check_NaN(row["اسپک قطعه"])
        scope_component.part_spec_certificate = check_NaN(row["اسپک قطعه مدرك"])
        scope_component.cover_spec = check_NaN(row["اسپك پوشش"])
        scope_component.cover_spec_certificate = check_NaN(row["اسپك پوشش مدرك"])
        scope_component.connections_spec = check_NaN(row["اسپك اتصالات"])
        scope_component.connections_spec_certificate = check_NaN(
            row["اسپك اتصالات مدرك"]
        )
        scope_component.other_specs_complementary_operations = check_NaN(
            row["ساير اسپك‌ها (عمليات تكميلي)"]
        )
        scope_component.other_specs_certificate = check_NaN(row["ساير اسپك‌ها مدرك"])
        scope_component.interprocess_maps = check_NaN(row["نقشه هاي ميان فرآيندي"])
        scope_component.interprocess_maps_certificate = check_NaN(
            row["نقشه هاي ميان فرآيندي مدرك"]
        )
        scope_component.rating_certificate = check_NaN(row["راتينگ مدرك"])
        scope_component.TP = check_NaN(row["TP"])
        scope_component.TP_certificate = check_NaN(row["TP مدرك"])
        scope_component.MQCP = check_NaN(row["MQCP"])
        scope_component.MQCP_certificate = check_NaN(row["MQCP مدرك"])
        scope_component.ITP = check_NaN(row["ITP"])
        scope_component.ITP_certificate = check_NaN(row["ITP مدرك"])
        scope_component.save()

    cols = _2_devices_side_df.columns
    col = cols[cols.str.contains("3885", na=True)].item()
    for index, value in _2_devices_side_df[col].items():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component._3885 = value
        scope_component.save()
    col = cols[cols.str.contains("Adv", na=False)].item()
    for index, value in _2_devices_side_df[col].items():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.adv_payment = value
        scope_component.save()

    for index, row in _2_devices_side_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.contract = check_NaN(row["Contract"])
        scope_component.material_supply = check_NaN(row["Material Supply"])
        scope_component.mold_or_die_or_fixture = check_NaN(row["Mold/Die/Fixture"])
        scope_component.casting = check_NaN(row["Casting"])
        scope_component.forge = check_NaN(row["Forge"])
        scope_component.forming = check_NaN(row["Forming"])
        scope_component.machining = check_NaN(row["Machining"])
        scope_component.brazing_or_welding = check_NaN(row["Brazing/Welding"])
        scope_component.coating = check_NaN(row["Coating"])
        scope_component.dummy_sample = check_NaN(row["Dummy sample"])
        scope_component.first_articles = (
            row["First Articles"] if row["First Articles"] else None,
        )
        scope_component.first_articles_test = check_NaN(row["First Articles Test"])
        scope_component._2_side_total_progress = check_NaN(row["Total Progress"])
        scope_component.save()

    for index, row in _28_devices_side_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.mass_production = check_NaN(row["Mass Production"])
        scope_component._28_side_total_progress = check_NaN(row["Total Progress"])
        scope_component.save()

    for index, row in _2_devices_manufacturing_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component._2_manufacturing_total_progress = check_NaN(
            row["Total Progress"]
        )
        scope_component.save()

    for index, row in _28_devices_manufacturing_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component._28_manufacturing_total_progress = check_NaN(
            row["Total Progress"]
        )
        scope_component.save()

    for index, row in _2_devices_quality_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.review_and_ITP_approval_4_percent = check_NaN(
            row["بررسی و \nتائید ITP \n(4%)"]
        )
        scope_component.qualitative_evaluation_the_contractor_2_percent = check_NaN(
            row["ارزيابي كيفي\n پيمانكار\n(2%)"]
        )
        scope_component.kick_off_meeting_3_percent = check_NaN(
            row["Kick Off \nMeeting\n(3%)"]
        )
        scope_component.CDR_5_percent = check_NaN(row["CDR\n(5%)"])
        scope_component.compliant_quality_inspection_ITP_or_MQCP_65_percent = check_NaN(
            row[" بازرسي كيفي مطابق\n ITP/MQCP\n(65%)"]
        )
        scope_component.submitting_an_inspection_report_accept_or_NCR_7_percent = (
            check_NaN(row["ارائه گزارش بازرسي\n Accept/NCR \n(7%)"])
        )
        scope_component.check_the_answer_design_to_NCR_5_percent = check_NaN(
            row["بررسي پاسخ \nطراحي به NCR \n(5%)"]
        )
        scope_component.issuing_quality_tag_2_percent = check_NaN(
            row["صدور\n تگ كيفي\n(2%)"]
        )
        scope_component.compilation_and_approval_final_book_5_percent = check_NaN(
            row[" تدوين و تاييد\n Final Book \n(5%)"]
        )
        scope_component.issuance_of_test_certificate_or_Form1_or_CoC_2_percent = (
            check_NaN(row["صدور Test Certificate\n/Form1/CoC \n(2%)"])
        )
        scope_component._2_quality_total_progress = check_NaN(
            row["میزان درصد \nپیشرفت"]
        )
        scope_component.save()

    for index, row in _28_devices_quality_df.iterrows():
        scope_component, created = ScopeComponent.objects.get_or_create(id=index + 1)
        scope_component.compliant_quality_inspection_ITP_or_MQCP_75_percent = check_NaN(
            row[" بازرسي كيفي مطابق\n ITP/MQCP\n(75%)"]
        )
        scope_component.submitting_an_inspection_report_accept_or_NCR_12_percent = (
            check_NaN(row["ارائه گزارش بازرسي\n Accept/NCR \n(12%)"])
        )
        scope_component.check_the_answer_design_to_NCR_3_percent = check_NaN(
            row["بررسي پاسخ \nطراحي به NCR \n(3%)"]
        )
        scope_component.issuing_quality_tag_2_percent = check_NaN(
            row["صدور\n تگ كيفي\n(2%)"]
        )
        scope_component.compilation_and_approval_final_book_6_percent = check_NaN(
            row[" تدوين و تاييد\n Final Book \n(6%)"]
        )
        scope_component.issuance_of_test_certificate_or_Form1_or_CoC_2_percent = (
            check_NaN(row["صدور Test Certificate\n/Form1/CoC \n(2%)"])
        )
        scope_component._28_quality_total_progress = check_NaN(row["درصد \nپیشرفت"])
        scope_component.save()

    bom_components = []
    for index, row in BOMdf.iterrows():
        bom_components.append(
            BomComponent(
                revision=check_NaN(row["REVISION"]),
                ID=check_NaN(row["ID"]),
                P_on_N_status_code=check_NaN(row["P/N Status Code"]),
                fig_no=check_NaN(row["Fig. No."]),
                item_no=check_NaN(row["Item No."]),
                module=check_NaN(row["Module"]),
                level=check_NaN(row["Level"]),
                code=check_NaN(row["Code"]),
                parent_code=check_NaN(row["Parent Code"]),
                part_number=check_NaN(row["Part Number"]),
                description=check_NaN(row["Description"]),
                comment=check_NaN(row["Comment"]),
                sap_name=check_NaN(row["SAP NAME"]),
                unit_per_assy=check_NaN(row["Units Per Assy"]),
                unit_per_end_item=check_NaN(row["Units Per End Item"]),
                corrected_units_per_end_item=check_NaN(
                    row["Corrected Units Per End Item"]
                ),
                gg_qty=check_NaN(row["GG QTY"]),
                srp=check_NaN(row["SRP"]),
                store_comment=check_NaN(row["Store Comment"]),
                assembly=True if row["Assembly"] == "yes" else False,
                standard_part=True if row["Standard Part"] == "yes" else False,
                material=check_NaN(row["Material"]),
                mfg_complexity_level=check_NaN(row["Mfg. Complexity Level"]),
                disassembled=check_NaN(row["Disassembled"]),
                supplying_or_manufacturing=check_NaN(row["Supplying / Manufacturing "]),
                internal_or_external_outsourcing=check_NaN(
                    row["Internal / External outsourcing"]
                ),
                vendor=check_NaN(row["Vendor"]),
                joining=check_NaN(row["Joining"]),
                manufacturing_process=check_NaN(row["Manufacturing Process"]),
                raw_material_form=check_NaN(row["Raw Material Form"]),
                function=check_NaN(row["Function"]),
                qc_criteria=check_NaN(row["QC Criteria"]),
                manufacturing_priority=check_NaN(row["Manufacturing Priority "]),
                manufacturing_responsible_department=check_NaN(
                    row["Manufacturing Responsible Department"]
                ),
                designing_responsible_department=check_NaN(
                    row["Designing Responsible Department"]
                ),
                usage_on_other_engines=check_NaN(row["USAGE ON OTHER ENGINES"]),
                manufacturing_parts_category=check_NaN(
                    row["MANUFACTURING PARTS Category"]
                ),
                scope_matrix_category=check_NaN(row["Scope Matrix Category"]),
                requires_manufacturing_or_supplying_for_reassembly=check_NaN(
                    row["Requires Manufacturing/Supplying For Re-Assembly"]
                ),
                system_D_requirements=check_NaN(row["System D. Requirement"]),
                percurment_state=check_NaN(row["PERCURMENT STATE"]),
                details=check_NaN(row["DETAILS"]),
                joint_type=check_NaN(row["Joint Type"]),
                discarded_during_disassembly=check_NaN(
                    row["DISCARDED DURING DISSASSEMBLY"]
                ),
                expendables=True if row["Expendables"] == "yes" else False,
                discarded_or_unusable_according_to_docs=check_NaN(
                    row["Discarded/Unusable According To Docs"]
                ),
                destroyed_for_analysis=check_NaN(row["Destroyed For Analysis"]),
                rejected_by_qc_or_inspection=check_NaN(
                    row["Rejected by QC/Inspection"]
                ),
                class_size_or_weight_as_required=check_NaN(
                    row["Class Size/Weight As Required"]
                ),
                EBOM=check_NaN(row["EBOM"]),
            )
        )
    BomComponent.objects.bulk_create(bom_components)

    provide_components = []
    for index, row in PROVIDEdf.iterrows():
        provide_components.append(
            ProvideComponent(
                application_type=check_NaN(row["نوع درخواست (گزارش خريد/قرارداد)"]),
                supply_stage=check_NaN(row["مرحله تامين"]),
                material_supplier=check_NaN(row["تامين كننده متريال"]),
                pr=check_NaN(row["شماره PR"]),
                po=check_NaN(row["شماره PO"]),
                subject=check_NaN(row["موضوع"]),
                request_type=check_NaN(row["جنس درخواست"]),
                customer_management=check_NaN(row["مديريت سفارش دهنده"]),
                contract_number=check_NaN(row["شماره قرارداد"]),
                supplier=check_NaN(row["تامين كننده"]),
                amount=check_NaN(row["مبلغ"]),
                adjustment_amount=check_NaN(row["مبلغ تعديل"]),
                currency=check_NaN(row["نوع ارز"]),
                expert=check_NaN(row["كارشناس مسئول"]),
                prepayment_percentage=check_NaN(row["درصد پيش‌پرداخت"]),
                currency_type=check_NaN(row["نوع ارز"]),
                prepayment_according_to_contract=check_NaN(
                    row["مبلغ پيش‌پرداخت طبق قرارداد"]
                ),
                prepaid_by_toga=check_NaN(row["پيش پرداخت توسط توگا"]),
                prepaid_by_air_engine=check_NaN(row["پيش پرداخت توسط موتور هوايي"]),
                prepayment_guarantee_check=check_NaN(row["چك تضمين پيش پرداخت"]),
                prepayment_guarantee=check_NaN(row["ضمانتنامه پيش پرداخت"]),
                mortgage_document_guarantee=check_NaN(row["ضمانت نامه سند رهني"]),
                financial_situation=check_NaN(row["وضعيت در معاونت مالي"]),
                prepayment_request_date=check_NaN(row["تاريخ درخواست پيش پرداخت"]),
                prepayment_amount=check_NaN(row["مبلغ پيش پرداخت"]),
                prepayment_date=check_NaN(row["تاريخ پرداخت پيش پرداخت"]),
            )
        )
    ProvideComponent.objects.bulk_create(provide_components)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_admin"),
    ]

    operations = [
        migrations.RunPython(create_default_group),
    ]
