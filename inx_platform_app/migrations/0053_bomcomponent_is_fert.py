# Generated by Django 4.2.4 on 2024-09-07 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0052_alter_productline_sqlapp_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="bomcomponent",
            name="is_fert",
            field=models.BooleanField(default=False),
        ),
    ]
