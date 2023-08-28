import os
import random

import pandas as pd
from django.db import migrations

script_dir = os.path.dirname(os.path.abspath(__file__))


def extract_initial_data():
    pass


def create_default_group(apps, schema_editor):
    BomComponent = apps.get_model("component", "BomComponent")
    Department = apps.get_model("user", "Department")
    BOMdf = pd.read_excel(os.path.join(script_dir, "..", "data", "EBOM.xlsx"))
    for index, row in BOMdf.iterrows():
        # designing_responsible_department = Department.objects.get(name__icontains=row["Designing Responsible Department"].replace(" ", ""))
        # manufacturing_responsible_department = Department.objects.get(name__icontains=row[
        #         "Manufacturing Responsible Department"
        #     ].replace(" ", ""))
        BomComponent.objects.create(
            revision=row["REVISION"],
            ID=row["ID"],
            P_on_N_status_code=row["P/N Status Code"],
            fig_no=row["Fig. No."],
            item_no=row["Item No."],
            module=row["Module"],
            level=row["Level"],
            code=row["Code"],
            parent_code=row["Parent Code"],
            part_number=row["Part Number"],
            description=row["Description"],
            comment=row["Comment"],
            sap_name=row["SAP NAME"],
            unit_per_assy=row["Units Per Assy"],
            unit_per_end_item=row["Units Per End Item"],
            corrected_units_per_end_item=row["Corrected Units Per End Item"],
            gg_qty=row["GG QTY"],
            srp=row["SRP"],
            store_comment=row["Store Comment"],
            assembly=True if row["Assembly"] == "yes" else False,
            standard_part=True if row["Standard Part"] == "yes" else False,
            material=row["Material"],
            mfg_complexity_level=row["Mfg. Complexity Level"],
            disassembled=row["Disassembled"],
            supplying_or_manufacturing=row["Supplying / Manufacturing "],
            internal_or_external_outsourcing=row["Internal / External outsourcing"],
            vendor=row["Vendor"],
            joining=row["Joining"],
            manufacturing_process=row["Manufacturing Process"],
            raw_material_form=row["Raw Material Form"],
            function=row["Function"],
            qc_criteria=row["QC Criteria"],
            manufacturing_priority=row["Manufacturing Priority "],
            manufacturing_responsible_department=row[
                "Manufacturing Responsible Department"
            ],
            designing_responsible_department=row["Designing Responsible Department"],
            usage_on_other_engines=row["USAGE ON OTHER ENGINES"],
            manufacturing_parts_category=row["MANUFACTURING PARTS Category"],
            scope_matrix_category=row["Scope Matrix Category"],
            requires_manufacturing_or_supplying_for_reassembly=row[
                "Requires Manufacturing/Supplying For Re-Assembly"
            ],
            system_D_requirements=row["System D. Requirement"],
            percurment_state=row["PERCURMENT STATE"],
            details=row["DETAILS"],
            joint_type=row["Joint Type"],
            discarded_during_disassembly=row["DISCARDED DURING DISSASSEMBLY"],
            expendables=True if row["Expendables"] == "yes" else False,
            discarded_or_unusable_according_to_docs=row[
                "Discarded/Unusable According To Docs"
            ],
            destroyed_for_analysis=row["Destroyed For Analysis"],
            rejected_by_qc_or_inspection=row["Rejected by QC/Inspection"],
            class_size_or_weight_as_required=row["Class Size/Weight As Required"],
            EBOM=row["EBOM"],
        )

    # instances = []
    # random_numbers = [random.randint(1, 1000) for _ in range(15000)]
    # for i in range(15000):
    #     instance = BomComponent(
    #         revision=random_numbers[i],
    #         ID=random_numbers[i],
    #         P_on_N_status_code=random_numbers[i],
    #         fig_no=random_numbers[i],
    #         item_no=random_numbers[i],
    #         module=random_numbers[i],
    #         level=random_numbers[i],
    #         code=random_numbers[i],
    #         parent_code=random_numbers[i],
    #         part_number=random_numbers[i],
    #         description=random_numbers[i],
    #         comment=random_numbers[i],
    #         sap_name=random_numbers[i],
    #         unit_per_assy=random_numbers[i],
    #         unit_per_end_item=random_numbers[i],
    #         corrected_units_per_end_item=random_numbers[i],
    #         gg_qty=random_numbers[i],
    #         srp=random_numbers[i],
    #         store_comment=random_numbers[i],
    #         assembly=True,
    #         standard_part=False,
    #         material=random_numbers[i],
    #         mfg_complexity_level=random_numbers[i],
    #         disassembled=random_numbers[i],
    #         supplying_or_manufacturing=random_numbers[i],
    #         internal_or_external_outsourcing=random_numbers[i],
    #         vendor=random_numbers[i],
    #         joining=random_numbers[i],
    #         manufacturing_process=random_numbers[i],
    #         raw_material_form=random_numbers[i],
    #         function=random_numbers[i],
    #         qc_criteria=random_numbers[i],
    #         manufacturing_priority=random_numbers[i],
    #         manufacturing_responsible_department=random_numbers[i],
    #         designing_responsible_department=random_numbers[i],
    #         usage_on_other_engines=random_numbers[i],
    #         manufacturing_parts_category=random_numbers[i],
    #         scope_matrix_category=random_numbers[i],
    #         requires_manufacturing_or_supplying_for_reassembly=random_numbers[i],
    #         system_D_requirements=random_numbers[i],
    #         percurment_state=random_numbers[i],
    #         details=random_numbers[i],
    #         joint_type=random_numbers[i],
    #         discarded_during_disassembly=random_numbers[i],
    #         expendables=True,
    #         discarded_or_unusable_according_to_docs=random_numbers[i],
    #         destroyed_for_analysis=random_numbers[i],
    #         rejected_by_qc_or_inspection=random_numbers[i],
    #         class_size_or_weight_as_required=random_numbers[i],
    #         EBOM=random_numbers[i],
    #     )
    #     instances.append(instance)
    # BomComponent.objects.bulk_create(instances)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_groups"),
    ]

    operations = [
        migrations.RunPython(create_default_group),
    ]
