# Generated by Django 4.2.4 on 2024-04-29 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0003_alter_order_product_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budfordetailline",
            name="detail_date",
            field=models.DateField(default="2024-01-01"),
        ),
        migrations.CreateModel(
            name="BudgetForecastDetails_sales",
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
                ("year", models.IntegerField(default=0, null=True)),
                ("month", models.IntegerField(default=0, null=True)),
                ("volume", models.IntegerField(default=0, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("value", models.IntegerField(default=0, null=True)),
                ("currency_zaq", models.CharField(max_length=3)),
                ("detail_date", models.DateField(default="2024-01-01")),
                ("sqlapp_id", models.IntegerField(default=0, null=True)),
                (
                    "budforline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inx_platform_app.budforline",
                    ),
                ),
                (
                    "scanario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inx_platform_app.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BudgetForecastDetails",
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
                ("year", models.IntegerField(default=0, null=True)),
                ("month", models.IntegerField(default=0, null=True)),
                ("volume", models.IntegerField(default=0, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("value", models.IntegerField(default=0, null=True)),
                ("currency_zaq", models.CharField(max_length=3)),
                ("detail_date", models.DateField(default="2024-01-01")),
                ("sqlapp_id", models.IntegerField(default=0, null=True)),
                (
                    "budforline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inx_platform_app.budforline",
                    ),
                ),
                (
                    "scanario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="inx_platform_app.scenario",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
