# Generated by Django 4.2.4 on 2024-06-06 07:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0016_alter_currency_symbol"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="currency",
            new_name="currency_text",
        ),
    ]