# Generated by Django 4.2.4 on 2024-05-29 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0012_alter_uploadedfilelog_celery_task_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="budgetforecastdetail",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.brand",
            ),
        ),
        migrations.AddField(
            model_name="budgetforecastdetail",
            name="color_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.colorgroup",
            ),
        ),
        migrations.AddField(
            model_name="budgetforecastdetail",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.customer",
            ),
        ),
        migrations.AddField(
            model_name="budgetforecastdetail_sales",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.brand",
            ),
        ),
        migrations.AddField(
            model_name="budgetforecastdetail_sales",
            name="color_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.colorgroup",
            ),
        ),
        migrations.AddField(
            model_name="budgetforecastdetail_sales",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.customer",
            ),
        ),
        migrations.AlterField(
            model_name="uploadedfile",
            name="process_status",
            field=models.CharField(
                choices=[
                    ("NEW", "new"),
                    ("PROCESSING", "processing"),
                    ("PROCESSED", "processed"),
                    ("ERROR", "error"),
                ],
                default="NEW",
                max_length=40,
            ),
        ),
    ]
