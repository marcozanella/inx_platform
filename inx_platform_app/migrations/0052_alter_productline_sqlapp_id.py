# Generated by Django 4.2.4 on 2024-09-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0051_bomheader_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productline",
            name="sqlapp_id",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
