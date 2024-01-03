# Generated by Django 4.2.4 on 2023-12-17 12:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0003_price_sales_org_price_scale_qty_from_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoredProcedure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("script", models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name="price",
            name="scale_qty_from",
        ),
        migrations.RemoveField(
            model_name="price",
            name="scale_qty_to",
        ),
    ]
