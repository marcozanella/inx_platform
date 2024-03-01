# Generated by Django 4.2.4 on 2024-02-29 21:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0020_contact_title"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contact",
            old_name="job_postion",
            new_name="job_position",
        ),
        migrations.AddField(
            model_name="contact",
            name="mobile_number",
            field=models.CharField(
                blank=True,
                max_length=20,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                        regex="^\\+?1?\\d{9,18}$",
                    )
                ],
            ),
        ),
    ]
