# Generated by Django 4.2.4 on 2024-08-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0037_bomcomponent_component_material_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_fert",
            field=models.BooleanField(default=False),
        ),
    ]
