# Generated by Django 4.2.4 on 2024-03-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inx_platform_app",
            "0036_rename_zacodmi9_import_line_zaqcodmi9_import_line_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="scenario",
            name="is_sales",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
