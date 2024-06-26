# Generated by Django 4.2.4 on 2024-06-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0014_scenario_is_budget_scenario_is_forecast_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
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
                ("name", models.CharField(max_length=30)),
                ("alpha_3", models.CharField(max_length=3)),
                ("symbol", models.CharField(max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name="exchangerate",
            name="currency",
            field=models.CharField(max_length=3, null=True),
        ),
    ]
