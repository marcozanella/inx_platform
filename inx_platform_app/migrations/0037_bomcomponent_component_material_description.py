# Generated by Django 4.2.4 on 2024-08-02 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inx_platform_app",
            "0036_bom_bomcomponent_bomheader_alter_brand_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="bomcomponent",
            name="component_material_description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
