# Generated by Django 4.2.4 on 2024-08-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0045_remove_product_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productstatus",
            name="color_a",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="productstatus",
            name="color_b",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="productstatus",
            name="color_g",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="productstatus",
            name="color_r",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="productstatus",
            name="sqlapp_id",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]