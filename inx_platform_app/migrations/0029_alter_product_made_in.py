# Generated by Django 4.2.4 on 2024-03-10 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0028_alter_product_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="made_in",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="inx_platform_app.madein",
            ),
        ),
    ]