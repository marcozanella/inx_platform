# Generated by Django 4.2.4 on 2024-02-26 13:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0014_alter_contact_customer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ke30line",
            old_name="disc_claims_adj_actual",
            new_name="disc_claim_adj_actual",
        ),
    ]
