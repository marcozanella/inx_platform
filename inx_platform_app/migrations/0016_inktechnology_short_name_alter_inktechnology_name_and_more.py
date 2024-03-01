# Generated by Django 4.2.4 on 2024-02-28 06:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "inx_platform_app",
            "0015_rename_disc_claims_adj_actual_ke30line_disc_claim_adj_actual",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="inktechnology",
            name="short_name",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="inktechnology",
            name="name",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name="inktechnology",
            name="sap_id",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="inktechnology",
            name="sap_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="inktechnology",
            name="sqlapp_id",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
