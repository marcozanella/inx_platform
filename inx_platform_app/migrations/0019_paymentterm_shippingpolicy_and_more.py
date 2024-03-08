# Generated by Django 4.2.4 on 2024-02-29 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "inx_platform_app",
            "0018_alter_majorlabel_sap_id_alter_majorlabel_sap_name_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentTerm",
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
                ("days_term", models.SmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ShippingPolicy",
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
                ("name", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="customer",
            name="customer_service_rep",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="ShippingAddress",
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
                ("name", models.CharField(max_length=250, null=True)),
                ("street_name", models.CharField(max_length=250, null=True)),
                ("street_number", models.CharField(max_length=250, null=True)),
                ("zip_code", models.CharField(max_length=250, null=True)),
                ("city", models.CharField(max_length=250, null=True)),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inx_platform_app.countrycode",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inx_platform_app.customer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="customer",
            name="payment_term",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="inx_platform_app.paymentterm",
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="shipping_policy",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.shippingpolicy",
            ),
        ),
    ]