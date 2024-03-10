# Generated by Django 4.2.4 on 2024-03-10 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0029_alter_product_made_in"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.brand",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="packaging",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.packaging",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_line",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.productline",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.productstatus",
            ),
        ),
    ]
