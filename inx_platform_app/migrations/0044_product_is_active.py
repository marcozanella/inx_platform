# Generated by Django 4.2.4 on 2024-08-05 14:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0043_alter_bom_item_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]