# Generated by Django 4.2.4 on 2024-07-16 15:49

from django.db import migrations, models
import inx_platform_app.models
import pathlib


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0031_alter_uploadedfilelog_file_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budgetforecastdetail",
            name="value",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="budgetforecastdetail",
            name="volume",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="budgetforecastdetail_sales",
            name="value",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="budgetforecastdetail_sales",
            name="volume",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="uploadedfilelog",
            name="file_path",
            field=models.FilePathField(
                blank=True,
                match=".*\\.(xlsx|XLSX)$",
                null=True,
                path=pathlib.PurePosixPath(
                    "/Users/marco/Library/CloudStorage/Dropbox/_dev/django_inx_platform/media_root"
                ),
                validators=[inx_platform_app.models.xls_xlsx_file_validator],
            ),
        ),
    ]
