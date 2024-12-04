# Generated by Django 4.2.4 on 2024-10-15 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0065_alter_uploadedfile_process_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="uploadedfile",
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Rebate",
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
                ("year", models.SmallIntegerField()),
                (
                    "rebate",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
                ),
                ("is_active", models.BooleanField(default=False)),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inx_platform_app.brand",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inx_platform_app.customer",
                    ),
                ),
                (
                    "scenario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inx_platform_app.scenario",
                    ),
                ),
            ],
        ),
    ]