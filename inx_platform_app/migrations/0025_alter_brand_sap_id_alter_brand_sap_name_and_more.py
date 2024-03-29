# Generated by Django 4.2.4 on 2024-03-01 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0024_alter_customer_approved_on"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="sap_id",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="brand",
            name="sap_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="brand",
            name="sqlapp_id",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="approved_on",
            field=models.DateField(blank=True, null=True),
        ),
    ]
