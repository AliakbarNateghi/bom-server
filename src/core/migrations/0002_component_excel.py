from django.db import migrations
import pandas as pd
import os
from ...component.models import BomComponent


script_dir = os.path.dirname(os.path.abspath(__file__))


def extract_initial_data():
    BOMdf = pd.read_excel(os.path.join(script_dir, ".", "data", "GT-22-BOM.xlsx"))
    for index, row in BOMdf.iterrows():
        product = BomComponent(
            revision=row["REVISION"],
            ID=row["ID"],
            P_on_N_status_code=row["P/N Status Code"],
            fig_no=row["Fig. No."],
            item_no=row["Item No."],
            module=row["Module"],
            level=row["Level"],
            part_number=row["Part Number"],
            description=row["Description"],
            unit_per_assy=row["Units Per Assy"],
            unit_per_end_item=row["Units Per End Item"],
            corrected_units_per_end_item=row["Corrected Units Per End Item"],
            gg_qty=row["GG QTY"],
            store_comment=row["Store Comment"],
            assembly=row["Assembly"],
            standard_part=row["Standard Part"],
            material=row["Material"],
            mfg_complexity_level=row["Mfg. Complexity Level"],
            disassembled=row["Disassembled"],
            supplying_and_manufacturing=row["Supplying / Manufacturing "],
            manufacturing_priority=row["Manufacturing Priority "],
            manufacturing_responsible_department=row["Manufacturing Responsible Department"],
            designing_responsible_department=row["Designing Responsible Department"],
            usage_on_other_engines=row["USAGE ON OTHER ENGINES"],
            manufacturing_parts_category=row["MANUFACTURING PARTS Category"],
            scope_matrix_category=row["Scope Matrix Category"],
            requires_manufacturing_or_supplying_for_reassembly=row["Requires Manufacturing/Supplying For Re-Assembly"],
            system_D_requirements=row["System D. Requirement"],
            percurment_state=row["PERCURMENT STATE"],
            details=row["DETAILS"],
            joint_type=row["Joint Type"],
            discarded_during_disassembly=row["DISCARDED DURING DISSASSEMBLY"],
            expendables=row["Expendables"],
            discarded_or_unusable_according_to_docs=row["Discarded/Unusable According To Docs"],
            destroyed_for_analysis=row["Destroyed For Analysis"],
            rejected_by_qc_or_inspection=row["Rejected by QC/Inspection"],
            class_size_or_weight_as_required=row["Class Size/Weight As Required"],
            EBOM=row["EBOM"],
        )

        


def create_default_group(apps, schema_editor):
    component = apps.get_model('component', 'BomComponent')
    

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_group),
    ]
