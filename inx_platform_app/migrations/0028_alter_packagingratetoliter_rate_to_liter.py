# Generated by Django 4.2.4 on 2024-07-09 11:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0027_packagingratetoliter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="packagingratetoliter",
            name="rate_to_liter",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
