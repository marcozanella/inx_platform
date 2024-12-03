# Generated by Django 4.2.4 on 2024-09-12 04:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inx_platform_app",
            "0058_rename_standard_price_per_kg_ea_bom_standard_price_per_kg_ea_czk_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="unitofmeasureconversionfactor",
            name="factor",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=15),
        ),
    ]
