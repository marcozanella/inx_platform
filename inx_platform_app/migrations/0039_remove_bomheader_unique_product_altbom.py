# Generated by Django 4.2.4 on 2024-08-02 14:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0038_product_is_fert"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="bomheader",
            name="unique_product_altbom",
        ),
    ]
